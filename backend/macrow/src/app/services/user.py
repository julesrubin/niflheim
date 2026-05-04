"""Firestore-backed single-user profile + goals.

One doc per user, keyed by user id. Today the only id in use is the literal
string `"me"`; when auth lands the same store serves uids unchanged. The
repository takes `user_id` as a parameter from day one so adding `/users/{id}`
later is a route-only change.
"""

import logging
from datetime import UTC, datetime

from google.api_core.exceptions import AlreadyExists
from google.cloud import firestore

from ..config.constants import FIRESTORE_USERS_COLLECTION
from ..models.user import User, UserPatch

logger = logging.getLogger(__name__)


def _seed_doc() -> dict:
    now = datetime.now(UTC)
    seed = User().model_dump(by_alias=False)
    seed["created_at"] = now
    seed["updated_at"] = now
    return seed


class UserRepository:
    def __init__(self, project: str | None, database: str) -> None:
        self._client = firestore.AsyncClient(project=project, database=database)
        self._users = self._client.collection(FIRESTORE_USERS_COLLECTION)

    async def get_or_create(self, user_id: str) -> dict:
        doc_ref = self._users.document(user_id)
        snap = await doc_ref.get()
        if snap.exists:
            return snap.to_dict() or _seed_doc()
        new_doc = _seed_doc()
        try:
            # create() 409s on race instead of clobbering — a concurrent caller
            # that just seeded the doc keeps their writes.
            await doc_ref.create(new_doc)
            return new_doc
        except AlreadyExists:
            snap = await doc_ref.get()
            return snap.to_dict() or _seed_doc()

    async def patch(self, user_id: str, patch: UserPatch) -> dict:
        """Apply non-None patch fields. Lazy-creates the doc if missing."""
        # exclude_none=True: explicit `null` from a client means "leave alone",
        # never "write None into a non-Optional storage field". Clear-to-default
        # is not a PATCH semantic on this surface.
        updates = patch.model_dump(
            exclude_unset=True, exclude_none=True, by_alias=False
        )
        if not updates:
            return await self.get_or_create(user_id)

        doc_ref = self._users.document(user_id)
        result: dict = {}

        @firestore.async_transactional
        async def _tx(transaction):
            nonlocal result
            snap = await doc_ref.get(transaction=transaction)
            # snap.to_dict() can be None even when snap.exists is True (empty
            # doc); fall back to a fresh seed in that case.
            doc = (snap.to_dict() or _seed_doc()) if snap.exists else _seed_doc()
            doc.update(updates)
            doc["updated_at"] = datetime.now(UTC)
            transaction.set(doc_ref, doc)
            result = doc

        await _tx(self._client.transaction())
        return result

    def close(self) -> None:
        self._client.close()
