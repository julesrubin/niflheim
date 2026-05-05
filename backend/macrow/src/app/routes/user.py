"""User profile + goals routes.

`/users/{user_id}` is the canonical resource. The bearer-token guard resolves
to a single user id today; the `owned_user_id` dependency 403s any path that
doesn't match the token. When auth grows to Firebase, the same dep starts
returning the verified `uid` claim — the route surface stays put.
"""

import logging

from fastapi import APIRouter, Depends

from ..auth import OwnedUserId
from ..models.user import User, UserPatch
from ..services.user import UserRepository
from ..utils.error import ERR_AUTH
from .deps import get_user_repo

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=User, responses={**ERR_AUTH})
async def get_user(
    user_id: OwnedUserId,
    repo: UserRepository = Depends(get_user_repo),
) -> User:
    doc = await repo.get_or_create(user_id)
    return _to_user(doc)


@router.patch("/{user_id}", response_model=User, responses={**ERR_AUTH})
async def patch_user(
    body: UserPatch,
    user_id: OwnedUserId,
    repo: UserRepository = Depends(get_user_repo),
) -> User:
    doc = await repo.patch(user_id, body)
    return _to_user(doc)


def _to_user(doc: dict) -> User:
    payload = {k: v for k, v in doc.items() if k not in {"created_at", "updated_at"}}
    return User.model_validate(payload)
