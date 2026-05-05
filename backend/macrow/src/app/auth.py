"""Authentication dependency — static bearer token, single user.

Designed so the future Firebase-Auth migration is a body-only swap of
`current_user_id`: the signature stays `(...) -> str` returning the user id,
the route surface (`Depends(current_user_id)` everywhere) stays untouched.

`HTTPBearer(auto_error=False)` is the right primitive here:
- it parses `Authorization: Bearer <token>` for us,
- registers a standard `bearerAuth` scheme in the OpenAPI schema (single-token
  Authorize dialog in `/docs`, no fictitious /token endpoint),
- `auto_error=False` lets us render the project's `{error: {code, message}}`
  envelope instead of FastAPI's default plain-text 403.

Future Firebase variant: replace the body of `current_user_id` with
`firebase_admin.auth.verify_id_token(creds.credentials)["uid"]` and drop
`CURRENT_USER_ID` from settings.
"""

import hmac
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .config.settings import settings
from .utils.error import forbidden_exc, unauthenticated_exc

bearer_scheme = HTTPBearer(auto_error=False, scheme_name="bearerAuth")


def current_user_id(
    creds: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> str:
    if creds is None or creds.scheme.lower() != "bearer":
        raise unauthenticated_exc("missing-token")
    expected = settings.BEARER_TOKEN.get_secret_value()
    if not hmac.compare_digest(creds.credentials, expected):
        raise unauthenticated_exc("invalid-token")
    return settings.CURRENT_USER_ID


CurrentUserId = Annotated[str, Depends(current_user_id)]


def owned_user_id(user_id: str, token_user_id: CurrentUserId) -> str:
    """Router-level dependency: 403 unless the path `user_id` matches the token's.

    Returns the (validated) user id so route handlers can take a single
    `user_id: Annotated[str, Depends(owned_user_id)]` and skip stitching the
    path param + token themselves. Mounted on routers with `prefix="/users/{user_id}"`
    via `dependencies=[Depends(owned_user_id)]` to gate every nested route.
    """
    if user_id != token_user_id:
        raise forbidden_exc()
    return token_user_id


OwnedUserId = Annotated[str, Depends(owned_user_id)]
