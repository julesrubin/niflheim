"""Firestore-backed cache of OFF products.

Stores a doc per barcode in collection `foods` (constant
FIRESTORE_FOODS_COLLECTION). The on-disk shape adds three internal fields
that are NOT part of the Food API model:

- name_lower: lowercased name, used for the prefix search range query.
- cached_at: set on first write, never updated.
- refreshed_at: bumped on every write — useful when we add a TTL job.

Search is prefix-only (Firestore has no full-text). For broader recall, the
/foods/search endpoint also queries OFF and merges by barcode.
"""

import logging
from datetime import UTC, datetime

from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

from ..config.constants import FIRESTORE_FOODS_COLLECTION
from ..models.food import Food
from .off import OffClient

logger = logging.getLogger(__name__)

# Firestore-internal fields stripped before returning Food rows.
_INTERNAL_FIELDS = frozenset({"name_lower", "cached_at", "refreshed_at"})

# End-of-range sentinel for Firestore prefix queries: a private-use
# code point past every Unicode char a normal product name would contain,
# so the half-open range [q, q + SENTINEL] is exactly "name starts with q".
_PREFIX_SENTINEL = "\uf8ff"


class FoodRepository:
    def __init__(self, project: str | None, database: str) -> None:
        self._client = firestore.AsyncClient(project=project, database=database)
        self._foods = self._client.collection(FIRESTORE_FOODS_COLLECTION)

    async def get_by_barcode(self, barcode: str) -> Food | None:
        snap = await self._foods.document(barcode).get()
        if not snap.exists:
            return None
        return _doc_to_food(snap.to_dict() or {})

    async def get_many(self, barcodes: list[str]) -> dict[str, Food]:
        """Batched read by barcode. Returns {barcode: Food} for hits; misses omitted.

        Lets callers (e.g. the journal route) embed Food into a list of items
        in a single round-trip rather than N sequential reads.
        """
        if not barcodes:
            return {}
        refs = [self._foods.document(b) for b in barcodes]
        out: dict[str, Food] = {}
        async for snap in self._client.get_all(refs):
            if snap.exists:
                out[snap.id] = _doc_to_food(snap.to_dict() or {})
        return out

    async def upsert(self, food: Food) -> None:
        """Create or refresh the doc; preserves cached_at on existing rows."""
        now = datetime.now(UTC)
        doc_ref = self._foods.document(food.barcode)

        existing = await doc_ref.get()
        cached_at = (
            existing.to_dict().get("cached_at")
            if existing.exists and existing.to_dict()
            else now
        )

        payload = food.model_dump(by_alias=False)
        # name_lower powers the prefix-range search; an empty string keeps the
        # row present in the index without matching any "starts with q" query.
        payload["name_lower"] = (food.name or "").lower()
        payload["cached_at"] = cached_at
        payload["refreshed_at"] = now

        await doc_ref.set(payload)

    async def search_by_name_prefix(self, q: str, limit: int) -> list[Food]:
        q_lower = q.lower()
        end = q_lower + _PREFIX_SENTINEL
        snaps = (
            await self._foods.where(filter=FieldFilter("name_lower", ">=", q_lower))
            .where(filter=FieldFilter("name_lower", "<=", end))
            .limit(limit)
            .get()
        )
        return [_doc_to_food(s.to_dict() or {}) for s in snaps]

    def close(self) -> None:
        self._client.close()


def _doc_to_food(data: dict) -> Food:
    cleaned = {k: v for k, v in data.items() if k not in _INTERNAL_FIELDS}
    return Food.model_validate(cleaned)


async def resolve_food(
    barcode: str,
    repo: FoodRepository,
    off: OffClient,
) -> Food | None:
    """Cache → OFF → upsert. Returns None if neither has the barcode.

    Shared between `GET /foods/{barcode}` and the journal `POST item` flow,
    where adding an item to a day must validate the barcode and prime the
    cache. Raises `OffUnavailable` on transport errors so the caller decides
    whether to surface 502 or degrade.
    """
    cached = await repo.get_by_barcode(barcode)
    if cached is not None:
        return cached
    product = await off.get_product(barcode)
    if product is None:
        return None
    await repo.upsert(product)
    return product
