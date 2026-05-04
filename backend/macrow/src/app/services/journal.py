"""Firestore-backed daily food journal.

One doc per day, keyed `YYYY-MM-DD`. Each doc carries four meal slots
(breakfast / lunch / dinner / snack); items are normalized — only
`{id, barcode, quantity, unit, checked}` is stored. Foods are joined in
by the route layer for read paths.

Mutations run inside Firestore transactions so concurrent iOS instances
can't lose updates.
"""

import logging
import uuid
from datetime import datetime, timezone

from google.cloud import firestore

from ..config.constants import FIRESTORE_JOURNAL_COLLECTION, MEAL_KINDS
from ..models.journal import LoggedFoodPatch, MealKind
from ..utils.error import JournalItemNotFound

logger = logging.getLogger(__name__)


def _empty_meals() -> dict[str, dict]:
    return {kind: {"items": []} for kind in MEAL_KINDS}


def _empty_day(date: str) -> dict:
    now = datetime.now(timezone.utc)
    return {
        "date": date,
        "meals": _empty_meals(),
        "created_at": now,
        "updated_at": now,
    }


class JournalRepository:
    def __init__(self, project: str | None, database: str) -> None:
        self._client = firestore.AsyncClient(project=project, database=database)
        self._days = self._client.collection(FIRESTORE_JOURNAL_COLLECTION)

    async def get_or_create(self, date: str) -> dict:
        """Read the day; if missing, write an empty 4-meal skeleton and return it."""
        doc_ref = self._days.document(date)
        snap = await doc_ref.get()
        if snap.exists:
            return snap.to_dict() or _empty_day(date)
        new_doc = _empty_day(date)
        await doc_ref.set(new_doc)
        return new_doc

    async def add_item(
        self,
        date: str,
        kind: MealKind,
        barcode: str,
        quantity: float,
        unit: str | None,
    ) -> dict:
        """Append a food-backed item to meals[kind].items. Lazy-creates the day."""
        item = {
            "id": str(uuid.uuid4()),
            "barcode": barcode,
            "quantity": quantity,
            "unit": unit,
            "checked": False,
        }
        await self._append_item(date, kind, item)
        return item

    async def add_recipe_item(
        self,
        date: str,
        kind: MealKind,
        recipe_id: str,
        servings: float,
    ) -> dict:
        """Append a recipe-backed item to meals[kind].items. Lazy-creates the day."""
        item = {
            "id": str(uuid.uuid4()),
            "recipe_id": recipe_id,
            "quantity": servings,
            "unit": "portion" if servings == 1 else "portions",
            "checked": False,
        }
        await self._append_item(date, kind, item)
        return item

    async def _append_item(self, date: str, kind: MealKind, item: dict) -> None:
        doc_ref = self._days.document(date)

        @firestore.async_transactional
        async def _tx(transaction):
            snap = await doc_ref.get(transaction=transaction)
            doc = snap.to_dict() if snap.exists else _empty_day(date)
            doc["meals"].setdefault(kind.value, {"items": []})["items"].append(item)
            doc["updated_at"] = datetime.now(timezone.utc)
            transaction.set(doc_ref, doc)

        await _tx(self._client.transaction())

    async def patch_item(
        self,
        date: str,
        item_id: str,
        patch: LoggedFoodPatch,
    ) -> dict:
        """Update an item by id. Raises JournalItemNotFound if absent on this day."""
        doc_ref = self._days.document(date)
        result: dict = {}

        @firestore.async_transactional
        async def _tx(transaction):
            nonlocal result
            snap = await doc_ref.get(transaction=transaction)
            if not snap.exists:
                raise JournalItemNotFound(item_id)
            doc = snap.to_dict() or {}
            updated = _apply_patch(doc, item_id, patch)
            if updated is None:
                raise JournalItemNotFound(item_id)
            doc["updated_at"] = datetime.now(timezone.utc)
            transaction.set(doc_ref, doc)
            result = updated

        await _tx(self._client.transaction())
        return result

    async def delete_items(self, date: str, item_ids: list[str]) -> None:
        """Remove items by id across all meal slots. Idempotent on unknown ids."""
        if not item_ids:
            return
        ids = set(item_ids)
        doc_ref = self._days.document(date)

        @firestore.async_transactional
        async def _tx(transaction):
            snap = await doc_ref.get(transaction=transaction)
            if not snap.exists:
                return
            doc = snap.to_dict() or {}
            removed = _pop_items(doc, ids)
            if not removed:
                return
            doc["updated_at"] = datetime.now(timezone.utc)
            transaction.set(doc_ref, doc)

        await _tx(self._client.transaction())

    async def move_items(
        self,
        from_date: str,
        item_ids: list[str],
        to_kind: MealKind,
        to_date: str | None,
    ) -> None:
        """Move items to a different meal (and optionally a different day).

        Same-day moves edit one doc; cross-day moves run a single transaction
        across the two day docs so the items can never appear twice or vanish.
        """
        if not item_ids:
            return
        target_date = to_date or from_date
        ids = set(item_ids)

        if target_date == from_date:
            doc_ref = self._days.document(from_date)

            @firestore.async_transactional
            async def _tx_same(transaction):
                snap = await doc_ref.get(transaction=transaction)
                if not snap.exists:
                    return
                doc = snap.to_dict() or {}
                moved = _pop_items(doc, ids)
                if not moved:
                    return
                _append_items(doc, to_kind.value, moved)
                doc["updated_at"] = datetime.now(timezone.utc)
                transaction.set(doc_ref, doc)

            await _tx_same(self._client.transaction())
            return

        src_ref = self._days.document(from_date)
        dst_ref = self._days.document(target_date)

        @firestore.async_transactional
        async def _tx_cross(transaction):
            src_snap = await src_ref.get(transaction=transaction)
            dst_snap = await dst_ref.get(transaction=transaction)
            if not src_snap.exists:
                return
            src_doc = src_snap.to_dict() or {}
            dst_doc = dst_snap.to_dict() if dst_snap.exists else _empty_day(target_date)
            moved = _pop_items(src_doc, ids)
            if not moved:
                return
            _append_items(dst_doc, to_kind.value, moved)
            now = datetime.now(timezone.utc)
            src_doc["updated_at"] = now
            dst_doc["updated_at"] = now
            transaction.set(src_ref, src_doc)
            transaction.set(dst_ref, dst_doc)

        await _tx_cross(self._client.transaction())

    def close(self) -> None:
        self._client.close()


def _apply_patch(doc: dict, item_id: str, patch: LoggedFoodPatch) -> dict | None:
    """Find item by id across all meals and apply non-None patch fields in place."""
    for kind in MEAL_KINDS:
        meal = doc["meals"].setdefault(kind, {"items": []})
        for item in meal["items"]:
            if item["id"] == item_id:
                if patch.checked is not None:
                    item["checked"] = patch.checked
                if patch.quantity is not None:
                    item["quantity"] = patch.quantity
                if patch.unit is not None:
                    item["unit"] = patch.unit
                return item
    return None


def _pop_items(doc: dict, ids: set[str]) -> list[dict]:
    """Remove items whose ids match from all meals; return them in iteration order."""
    popped: list[dict] = []
    for kind in MEAL_KINDS:
        meal = doc["meals"].setdefault(kind, {"items": []})
        kept: list[dict] = []
        for item in meal["items"]:
            if item["id"] in ids:
                popped.append(item)
            else:
                kept.append(item)
        meal["items"] = kept
    return popped


def _append_items(doc: dict, kind: str, items: list[dict]) -> None:
    doc["meals"].setdefault(kind, {"items": []})["items"].extend(items)
