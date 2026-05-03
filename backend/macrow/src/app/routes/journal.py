"""Daily food journal — read, log, edit, delete, and move items.

Storage is one Firestore doc per day. Each route validates the path date /
meal-kind, delegates to `JournalRepository`, and embeds the cached Food on
read paths via `FoodRepository.get_many` so the iOS client gets everything
in one HTTP round-trip.
"""

import logging
from datetime import datetime

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse

from ..models.food import Food
from ..models.journal import (
    BulkDeleteRequest,
    DailyJournal,
    LoggedFood,
    LoggedFoodCreate,
    LoggedFoodPatch,
    Meal,
    MealKind,
    MoveItemsRequest,
)
from ..services.food import FoodRepository, resolve_food
from ..services.journal import JournalRepository
from ..services.off import OffClient
from ..utils.error import (
    JournalItemNotFound,
    OffUnavailable,
    barcode_not_found,
    invalid_date,
    invalid_meal_kind,
    journal_item_not_found,
    off_unavailable,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/journal", tags=["journal"])


def get_off(request: Request) -> OffClient:
    return request.app.state.off_client


def get_food_repo(request: Request) -> FoodRepository:
    return request.app.state.food_repo


def get_journal_repo(request: Request) -> JournalRepository:
    return request.app.state.journal_repo


@router.get("/days/{date}", response_model=DailyJournal)
async def get_journal_day(
    date: str,
    journal: JournalRepository = Depends(get_journal_repo),
    foods: FoodRepository = Depends(get_food_repo),
) -> DailyJournal | JSONResponse:
    if not _is_valid_date(date):
        return invalid_date(date)
    doc = await journal.get_or_create(date)
    food_map = await _load_foods(foods, doc)
    return _shape_day(doc, food_map)


@router.post("/days/{date}/meals/{kind}/items", response_model=LoggedFood)
async def add_journal_item(
    date: str,
    kind: str,
    body: LoggedFoodCreate,
    journal: JournalRepository = Depends(get_journal_repo),
    foods: FoodRepository = Depends(get_food_repo),
    off: OffClient = Depends(get_off),
) -> LoggedFood | JSONResponse:
    if not _is_valid_date(date):
        return invalid_date(date)
    meal_kind = _to_meal_kind(kind)
    if meal_kind is None:
        return invalid_meal_kind(kind, tuple(k.value for k in MealKind))

    try:
        food = await resolve_food(body.barcode, foods, off)
    except OffUnavailable:
        return off_unavailable()
    if food is None:
        return barcode_not_found(body.barcode)

    item = await journal.add_item(
        date=date,
        kind=meal_kind,
        barcode=body.barcode,
        quantity=body.quantity,
        unit=body.unit,
    )
    return _to_logged_food(item, food)


@router.patch("/days/{date}/items/{item_id}", response_model=LoggedFood)
async def patch_journal_item(
    date: str,
    item_id: str,
    patch: LoggedFoodPatch,
    journal: JournalRepository = Depends(get_journal_repo),
    foods: FoodRepository = Depends(get_food_repo),
) -> LoggedFood | JSONResponse:
    if not _is_valid_date(date):
        return invalid_date(date)
    try:
        item = await journal.patch_item(date, item_id, patch)
    except JournalItemNotFound:
        return journal_item_not_found(item_id)

    food_map = await foods.get_many([item["barcode"]])
    food = food_map.get(item["barcode"])
    if food is None:
        # Stale ref — the cache lost the food. Surface as 404 so the client
        # drops the item rather than silently rendering it without macros.
        logger.warning(
            "Patched item %s references missing food %s", item_id, item["barcode"]
        )
        return barcode_not_found(item["barcode"])
    return _to_logged_food(item, food)


@router.delete("/days/{date}/items/{item_id}", response_model=None)
async def delete_journal_item(
    date: str,
    item_id: str,
    journal: JournalRepository = Depends(get_journal_repo),
) -> Response | JSONResponse:
    if not _is_valid_date(date):
        return invalid_date(date)
    await journal.delete_items(date, [item_id])
    return Response(status_code=204)


@router.post("/days/{date}/items:bulk-delete", response_model=None)
async def bulk_delete_journal_items(
    date: str,
    body: BulkDeleteRequest,
    journal: JournalRepository = Depends(get_journal_repo),
) -> Response | JSONResponse:
    if not _is_valid_date(date):
        return invalid_date(date)
    await journal.delete_items(date, body.item_ids)
    return Response(status_code=204)


@router.post("/days/{date}/items:move", response_model=None)
async def move_journal_items(
    date: str,
    body: MoveItemsRequest,
    journal: JournalRepository = Depends(get_journal_repo),
) -> Response | JSONResponse:
    if not _is_valid_date(date):
        return invalid_date(date)
    if body.to_date is not None and not _is_valid_date(body.to_date):
        return invalid_date(body.to_date)
    await journal.move_items(
        from_date=date,
        item_ids=body.item_ids,
        to_kind=body.to_kind,
        to_date=body.to_date,
    )
    return Response(status_code=204)


# ─── helpers ────────────────────────────────────────────────────────────────


def _is_valid_date(value: str) -> bool:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return False
    return True


def _to_meal_kind(value: str) -> MealKind | None:
    try:
        return MealKind(value)
    except ValueError:
        return None


async def _load_foods(repo: FoodRepository, doc: dict) -> dict[str, Food]:
    """Collect unique barcodes from all four meals and batch-read them."""
    meals = doc.get("meals") or {}
    barcodes = {
        item["barcode"] for meal in meals.values() for item in meal.get("items", [])
    }
    if not barcodes:
        return {}
    return await repo.get_many(list(barcodes))


def _shape_day(doc: dict, foods: dict[str, Food]) -> DailyJournal:
    """Build the wire-shape DailyJournal, dropping items whose food has been evicted."""
    storage_meals = doc.get("meals") or {}
    meals: list[Meal] = []
    for kind in MealKind:
        raw_items = (storage_meals.get(kind.value) or {}).get("items", [])
        items: list[LoggedFood] = []
        for raw in raw_items:
            food = foods.get(raw["barcode"])
            if food is None:
                logger.warning(
                    "Dropping item %s on %s: barcode %s no longer in cache",
                    raw["id"],
                    doc.get("date"),
                    raw["barcode"],
                )
                continue
            items.append(_to_logged_food(raw, food))
        meals.append(Meal(kind=kind, items=items))
    return DailyJournal(date=doc["date"], meals=meals)


def _to_logged_food(raw: dict, food: Food) -> LoggedFood:
    return LoggedFood(
        id=raw["id"],
        barcode=raw["barcode"],
        quantity=raw["quantity"],
        unit=raw.get("unit"),
        checked=raw.get("checked", False),
        food=food,
    )
