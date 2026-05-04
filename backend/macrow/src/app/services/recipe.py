"""Firestore-backed recipe storage.

One doc per recipe, keyed by server-generated UUID. Recipes are user-mutable;
historical journal entries that reference a deleted recipe surface the
missing-ref via the `routes/journal._shape_day` warn-and-drop path, matching
the existing food-eviction handling.
"""

import logging
import uuid
from datetime import datetime, timezone

from google.cloud import firestore

from ..config.constants import FIRESTORE_RECIPES_COLLECTION
from ..models.recipe import Recipe, RecipeCreate, RecipePatch
from ..utils.error import RecipeNotFound

logger = logging.getLogger(__name__)

_INTERNAL_FIELDS = frozenset({"created_at", "updated_at"})


def _doc_to_recipe(data: dict) -> Recipe:
    cleaned = {k: v for k, v in data.items() if k not in _INTERNAL_FIELDS}
    return Recipe.model_validate(cleaned)


class RecipeRepository:
    def __init__(self, project: str | None, database: str) -> None:
        self._client = firestore.AsyncClient(project=project, database=database)
        self._recipes = self._client.collection(FIRESTORE_RECIPES_COLLECTION)

    async def create(self, body: RecipeCreate) -> Recipe:
        recipe_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        doc = body.model_dump(by_alias=False)
        doc.update({"id": recipe_id, "created_at": now, "updated_at": now})
        await self._recipes.document(recipe_id).set(doc)
        return _doc_to_recipe(doc)

    async def get(self, recipe_id: str) -> Recipe | None:
        snap = await self._recipes.document(recipe_id).get()
        if not snap.exists:
            return None
        return _doc_to_recipe(snap.to_dict() or {})

    async def get_many(self, recipe_ids: list[str]) -> dict[str, Recipe]:
        if not recipe_ids:
            return {}
        refs = [self._recipes.document(i) for i in recipe_ids]
        out: dict[str, Recipe] = {}
        async for snap in self._client.get_all(refs):
            if snap.exists:
                out[snap.id] = _doc_to_recipe(snap.to_dict() or {})
        return out

    async def list_all(self) -> list[Recipe]:
        snaps = await self._recipes.get()
        return [_doc_to_recipe(s.to_dict() or {}) for s in snaps]

    async def patch(self, recipe_id: str, patch: RecipePatch) -> Recipe:
        # exclude_none=True: explicit `null` from a client means "leave alone",
        # never "write None into a non-Optional storage field". Clear-to-default
        # is not a PATCH semantic on this surface.
        updates = patch.model_dump(
            exclude_unset=True, exclude_none=True, by_alias=False
        )
        if not updates:
            existing = await self.get(recipe_id)
            if existing is None:
                raise RecipeNotFound(recipe_id)
            return existing

        doc_ref = self._recipes.document(recipe_id)
        result: Recipe | None = None

        @firestore.async_transactional
        async def _tx(transaction):
            nonlocal result
            snap = await doc_ref.get(transaction=transaction)
            if not snap.exists:
                raise RecipeNotFound(recipe_id)
            doc = snap.to_dict() or {}
            doc.update(updates)
            doc["updated_at"] = datetime.now(timezone.utc)
            transaction.set(doc_ref, doc)
            result = _doc_to_recipe(doc)

        await _tx(self._client.transaction())
        assert result is not None
        return result

    async def delete(self, recipe_id: str) -> bool:
        """Returns True if a doc was removed, False if it didn't exist."""
        doc_ref = self._recipes.document(recipe_id)
        snap = await doc_ref.get()
        if not snap.exists:
            return False
        await doc_ref.delete()
        return True

    def close(self) -> None:
        self._client.close()
