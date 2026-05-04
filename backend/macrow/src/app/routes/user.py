"""User profile + goals routes.

`/users/me` is the alias for the current user. When auth lands, `me` resolves
against the token and `/users/{user_id}` joins the surface for cross-user
fetches — neither the model nor the repository changes, only this layer.
"""

import logging

from fastapi import APIRouter, Depends

from ..models.user import User, UserPatch
from ..services.user import UserRepository
from .deps import get_user_repo

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["users"])

# Resolved against the auth token once auth lands; for now a fixed string.
CURRENT_USER_ID = "me"


@router.get("/me", response_model=User)
async def get_current_user(repo: UserRepository = Depends(get_user_repo)) -> User:
    doc = await repo.get_or_create(CURRENT_USER_ID)
    return _to_user(doc)


@router.patch("/me", response_model=User)
async def patch_current_user(
    body: UserPatch,
    repo: UserRepository = Depends(get_user_repo),
) -> User:
    doc = await repo.patch(CURRENT_USER_ID, body)
    return _to_user(doc)


def _to_user(doc: dict) -> User:
    payload = {k: v for k, v in doc.items() if k not in {"created_at", "updated_at"}}
    return User.model_validate(payload)
