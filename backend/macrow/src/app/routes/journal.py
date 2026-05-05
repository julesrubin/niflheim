"""Daily food journal — read, log, edit, delete, and move items.

Storage is one Firestore doc per day. Each route validates the path date /
meal-kind, delegates to `JournalRepository`, and embeds the cached Food OR the
referenced Recipe on read paths so the iOS client gets everything in one HTTP
round-trip.

A logged item is either food-backed (barcode + Food) or recipe-backed
(recipe_id + Recipe). Exactly one ref is stored per item; embed-on-read joins
to whichever cache the item points at.
"""

import asyncio
import logging
from datetime import date

from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse

from ..models.food import Food
from ..models.journal import (
    BulkDeleteRequest,
    DailyJournal,
    LoggedFood,
    LoggedFoodCreate,
    LoggedFoodPatch,
    LoggedRecipeCreate,
    Meal,
    MealKind,
    MoveItemsRequest,
)
from ..models.recipe import Recipe
from ..services.food import FoodRepository, resolve_food
from ..services.journal import JournalRepository
from ..services.off import OffClient
from ..services.recipe import RecipeRepository, compute_macros
from .deps import get_food_repo, get_journal_repo, get_off, get_recipe_repo
from ..utils.error import (
    ERR_400,
    ERR_404,
    ERR_502,
    JournalItemNotFound,
    OffUnavailable,
    barcode_not_found,
    invalid_date,
    invalid_meal_kind,
    journal_item_not_found,
    off_unavailable,
    recipe_not_found,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/journal", tags=["journal"])

_ALLOWED_MEAL_KINDS: tuple[str, ...] = tuple(k.value for k in MealKind)


@router.get(
    "/days/{date}",
    response_model=DailyJournal,
    responses={**ERR_400},
    summary="Get the journal for a single day",
)
async def get_journal_day(
    date: str,
    journal: JournalRepository = Depends(get_journal_repo),
    foods: FoodRepository = Depends(get_food_repo),
    recipes: RecipeRepository = Depends(get_recipe_repo),
) -> DailyJournal | JSONResponse:
    if not _is_valid_date(date):
        return invalid_date(date)
    doc = await journal.get_or_create(date)
    food_map, recipe_map = await _load_refs(foods, recipes, doc)
    return _shape_day(doc, food_map, recipe_map)


@router.post(
    "/days/{date}/meals/{kind}/items",
    response_model=LoggedFood,
    responses={**ERR_400, **ERR_404, **ERR_502},
    summary="Log a barcode-backed food into a meal",
)
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
        return invalid_meal_kind(kind, _ALLOWED_MEAL_KINDS)

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
    )
    return _to_logged_food(item, food=food)


@router.post(
    "/days/{date}/meals/{kind}/recipes",
    response_model=LoggedFood,
    responses={**ERR_400, **ERR_404},
    summary="Log a recipe-backed item into a meal",
)
async def add_journal_recipe(
    date: str,
    kind: str,
    body: LoggedRecipeCreate,
    journal: JournalRepository = Depends(get_journal_repo),
    recipes: RecipeRepository = Depends(get_recipe_repo),
    foods: FoodRepository = Depends(get_food_repo),
) -> LoggedFood | JSONResponse:
    if not _is_valid_date(date):
        return invalid_date(date)
    meal_kind = _to_meal_kind(kind)
    if meal_kind is None:
        return invalid_meal_kind(kind, _ALLOWED_MEAL_KINDS)

    recipe = await recipes.get(body.recipe_id)
    if recipe is None:
        return recipe_not_found(body.recipe_id)
    food_map = await foods.get_many([i.barcode for i in recipe.ingredients])
    recipe = compute_macros(recipe, food_map)

    item = await journal.add_recipe_item(
        date=date,
        kind=meal_kind,
        recipe_id=body.recipe_id,
        servings=body.servings,
    )
    return _to_logged_food(item, recipe=recipe)


@router.patch(
    "/days/{date}/items/{item_id}",
    response_model=LoggedFood,
    responses={**ERR_400, **ERR_404},
    summary="Update a logged item (check off / change quantity)",
)
async def patch_journal_item(
    date: str,
    item_id: str,
    patch: LoggedFoodPatch,
    journal: JournalRepository = Depends(get_journal_repo),
    foods: FoodRepository = Depends(get_food_repo),
    recipes: RecipeRepository = Depends(get_recipe_repo),
) -> LoggedFood | JSONResponse:
    if not _is_valid_date(date):
        return invalid_date(date)
    try:
        item = await journal.patch_item(date, item_id, patch)
    except JournalItemNotFound:
        return journal_item_not_found(item_id)

    # The storage write already succeeded — never 404 after that. Missing refs
    # surface as null on the embed, matching _shape_day's warn-drop tolerance.
    if item.get("recipe_id"):
        recipe = await recipes.get(item["recipe_id"])
        if recipe is None:
            logger.warning(
                "Patched item %s references missing recipe %s",
                item_id,
                item["recipe_id"],
            )
        else:
            ingredient_foods = await foods.get_many(
                [i.barcode for i in recipe.ingredients]
            )
            recipe = compute_macros(recipe, ingredient_foods)
        return _to_logged_food(item, recipe=recipe)

    barcode = item.get("barcode")
    if barcode is None:
        # Should not happen — POST validates; surface clearly if it ever does.
        logger.error("Patched item %s has neither barcode nor recipe_id", item_id)
        return journal_item_not_found(item_id)
    food_map = await foods.get_many([barcode])
    food = food_map.get(barcode)
    if food is None:
        logger.warning("Patched item %s references missing food %s", item_id, barcode)
    return _to_logged_food(item, food=food)


@router.delete(
    "/days/{date}/items/{item_id}",
    response_model=None,
    responses={**ERR_400},
    status_code=204,
    summary="Delete a single logged item",
)
async def delete_journal_item(
    date: str,
    item_id: str,
    journal: JournalRepository = Depends(get_journal_repo),
) -> Response | JSONResponse:
    if not _is_valid_date(date):
        return invalid_date(date)
    await journal.delete_items(date, [item_id])
    return Response(status_code=204)


@router.post(
    "/days/{date}/items:bulk-delete",
    response_model=None,
    responses={**ERR_400},
    status_code=204,
    summary="Delete multiple logged items in one call",
)
async def bulk_delete_journal_items(
    date: str,
    body: BulkDeleteRequest,
    journal: JournalRepository = Depends(get_journal_repo),
) -> Response | JSONResponse:
    if not _is_valid_date(date):
        return invalid_date(date)
    await journal.delete_items(date, body.item_ids)
    return Response(status_code=204)


@router.post(
    "/days/{date}/items:move",
    response_model=None,
    responses={**ERR_400},
    status_code=204,
    summary="Move items between meals or to another day",
)
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
    """Accept only YYYY-MM-DD. date.fromisoformat() in 3.11+ also accepts the
    compact form 'YYYYMMDD'; round-tripping through .isoformat() rules that out
    so storage doc-ids stay consistent."""
    try:
        return date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def _to_meal_kind(value: str) -> MealKind | None:
    """Path-level meal-kind validation done in the handler, not the route
    signature. Declaring `kind: MealKind` would let FastAPI auto-validate, but
    its 422 envelope diverges from the project's standard {error: {code, ...}}
    shape — keeping validation in the handler lets every 4xx use the same
    envelope via invalid_meal_kind()."""
    try:
        return MealKind(value)
    except ValueError:
        return None


async def _load_refs(
    food_repo: FoodRepository,
    recipe_repo: RecipeRepository,
    doc: dict,
) -> tuple[dict[str, Food], dict[str, Recipe]]:
    """Collect refs across all meals, batch-read both, then decorate recipes
    with computed per-serving macros (which needs a second pass over any
    ingredient foods not already loaded for direct food-backed items)."""
    meals = doc.get("meals") or {}
    barcodes: set[str] = set()
    recipe_ids: set[str] = set()
    for meal in meals.values():
        for item in meal.get("items", []):
            if item.get("barcode"):
                barcodes.add(item["barcode"])
            if item.get("recipe_id"):
                recipe_ids.add(item["recipe_id"])
    foods, recipes = await asyncio.gather(
        food_repo.get_many(list(barcodes)),
        recipe_repo.get_many(list(recipe_ids)),
    )

    # Recipes need their ingredient foods to compute macros — fetch the
    # delta against what we already loaded for direct food-backed items.
    ingredient_barcodes = {
        ing.barcode for r in recipes.values() for ing in r.ingredients
    }
    missing = list(ingredient_barcodes - foods.keys())
    if missing:
        foods = {**foods, **(await food_repo.get_many(missing))}

    decorated_recipes = {rid: compute_macros(r, foods) for rid, r in recipes.items()}
    return foods, decorated_recipes


def _shape_day(
    doc: dict,
    foods: dict[str, Food],
    recipes: dict[str, Recipe],
) -> DailyJournal:
    """Build the wire-shape DailyJournal, dropping items whose ref has been evicted."""
    storage_meals = doc.get("meals") or {}
    meals: list[Meal] = []
    for kind in MealKind:
        raw_items = (storage_meals.get(kind.value) or {}).get("items", [])
        items: list[LoggedFood] = []
        for raw in raw_items:
            if raw.get("recipe_id"):
                recipe = recipes.get(raw["recipe_id"])
                if recipe is None:
                    logger.warning(
                        "Dropping item %s on %s: recipe %s no longer in store",
                        raw["id"],
                        doc.get("date"),
                        raw["recipe_id"],
                    )
                    continue
                items.append(_to_logged_food(raw, recipe=recipe))
                continue

            barcode = raw.get("barcode")
            if barcode is None:
                logger.warning(
                    "Dropping item %s on %s: no barcode and no recipe_id",
                    raw["id"],
                    doc.get("date"),
                )
                continue
            food = foods.get(barcode)
            if food is None:
                logger.warning(
                    "Dropping item %s on %s: barcode %s no longer in cache",
                    raw["id"],
                    doc.get("date"),
                    barcode,
                )
                continue
            items.append(_to_logged_food(raw, food=food))
        meals.append(Meal(kind=kind, items=items))
    return DailyJournal(date=doc["date"], meals=meals)


def _to_logged_food(
    raw: dict,
    *,
    food: Food | None = None,
    recipe: Recipe | None = None,
) -> LoggedFood:
    return LoggedFood(
        id=raw["id"],
        quantity=raw["quantity"],
        checked=raw.get("checked", False),
        barcode=raw.get("barcode"),
        food=food,
        recipe_id=raw.get("recipe_id"),
        recipe=recipe,
    )
