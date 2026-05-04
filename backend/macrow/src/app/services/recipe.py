"""Firestore-backed recipe storage.

One doc per recipe, keyed by server-generated UUID. Recipes are user-mutable;
historical journal entries that reference a deleted recipe surface the
missing-ref via the `routes/journal._shape_day` warn-and-drop path, matching
the existing food-eviction handling.

Per-serving macros are NOT stored — `compute_macros()` derives them on read by
joining ingredients to the foods cache. See `models/recipe.Recipe` for the
contract.
"""

import logging
import uuid
from datetime import UTC, datetime

from google.cloud import firestore

from ..config.constants import FIRESTORE_RECIPES_COLLECTION
from ..models.food import Food
from ..models.recipe import Recipe, RecipeCreate, RecipePatch
from ..utils.error import RecipeNotFound

logger = logging.getLogger(__name__)

_INTERNAL_FIELDS = frozenset({"created_at", "updated_at"})


def _doc_to_recipe(data: dict) -> Recipe:
    cleaned = {k: v for k, v in data.items() if k not in _INTERNAL_FIELDS}
    return Recipe.model_validate(cleaned)


def compute_macros(recipe: Recipe, foods: dict[str, Food]) -> Recipe:
    """Return a copy of `recipe` with per-serving macros computed.

    Sums ingredient.quantity × food.macro / 100 across ingredients and divides
    by servings. Ingredients whose barcode is missing from the cache are
    skipped with a warning; nutrition_complete is False so the client knows
    the totals are partial.
    """
    if not recipe.ingredients:
        return recipe.model_copy(update={"nutrition_complete": True})

    cals = prot = carb = fat_ = 0.0
    complete = True
    for ing in recipe.ingredients:
        food = foods.get(ing.barcode)
        if food is None:
            logger.warning(
                "Recipe %s ingredient %s missing from cache; macros partial",
                recipe.id,
                ing.barcode,
            )
            complete = False
            continue
        # food.* are per 100 units of food.base_unit; quantity is in the same.
        factor = ing.quantity / 100
        cals += food.calories * factor
        prot += food.protein * factor
        carb += food.carbs * factor
        fat_ += food.fat * factor

    servings = recipe.servings
    return recipe.model_copy(
        update={
            "calories_per_serving": int(round(cals / servings)),
            "protein_per_serving": round(prot / servings, 1),
            "carbs_per_serving": round(carb / servings, 1),
            "fat_per_serving": round(fat_ / servings, 1),
            "nutrition_complete": complete,
        }
    )


class RecipeRepository:
    def __init__(self, project: str | None, database: str) -> None:
        self._client = firestore.AsyncClient(project=project, database=database)
        self._recipes = self._client.collection(FIRESTORE_RECIPES_COLLECTION)

    async def create(self, body: RecipeCreate) -> Recipe:
        recipe_id = str(uuid.uuid4())
        now = datetime.now(UTC)
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
            doc["updated_at"] = datetime.now(UTC)
            transaction.set(doc_ref, doc)
            result = _doc_to_recipe(doc)

        await _tx(self._client.transaction())
        if result is None:
            # Should be unreachable: the transaction body either sets `result`
            # or raises RecipeNotFound which would propagate above.
            raise RuntimeError("transaction returned without setting result")
        return result

    async def delete(self, recipe_id: str) -> None:
        """Idempotent delete — Firestore treats deleting a missing doc as a no-op,
        so a read-first guard would only add a TOCTOU window and a round-trip."""
        await self._recipes.document(recipe_id).delete()

    def close(self) -> None:
        self._client.close()
