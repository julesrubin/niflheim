"""FastAPI application factory."""

import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from .auth import owned_user_id
from .config.settings import settings
from .models.common import ApiError, ApiErrorResponse
from .routes import foods, health, journal, recipe, user
from .services.food import FoodRepository
from .services.journal import JournalRepository
from .services.off import OffClient
from .services.recipe import RecipeRepository
from .services.user import UserRepository
from .utils.error import EnvelopeHTTPException

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Build long-lived clients once and stash them on app.state.

    Routes pull these via Depends so we never pay per-request connection
    setup. The Firestore client lazily opens gRPC channels on first call.
    """
    app.state.off_client = OffClient(
        base_url=settings.OFF_BASE_URL,
        search_base_url=settings.OFF_SEARCH_BASE_URL,
        user_agent=settings.OFF_USER_AGENT,
        timeout=settings.OFF_TIMEOUT_SECONDS,
    )
    app.state.food_repo = FoodRepository(
        project=settings.FIRESTORE_PROJECT,
        database=settings.FIRESTORE_DATABASE,
    )
    app.state.journal_repo = JournalRepository(
        project=settings.FIRESTORE_PROJECT,
        database=settings.FIRESTORE_DATABASE,
    )
    app.state.user_repo = UserRepository(
        project=settings.FIRESTORE_PROJECT,
        database=settings.FIRESTORE_DATABASE,
    )
    app.state.recipe_repo = RecipeRepository(
        project=settings.FIRESTORE_PROJECT,
        database=settings.FIRESTORE_DATABASE,
    )
    logger.info(
        "Lifespan ready: OFF=%s firestore=%s/%s",
        settings.OFF_BASE_URL,
        settings.FIRESTORE_PROJECT or "<adc-default>",
        settings.FIRESTORE_DATABASE,
    )
    try:
        yield
    finally:
        # Each close is independent; one failure must not skip the others or
        # we leak gRPC channels (and on local dev / pytest, hang the runner).
        closers = (
            app.state.off_client.aclose,
            app.state.food_repo.close,
            app.state.journal_repo.close,
            app.state.user_repo.close,
            app.state.recipe_repo.close,
        )
        for closer in closers:
            try:
                result = closer()
                if asyncio.iscoroutine(result):
                    await result
            except Exception:
                logger.exception("Lifespan teardown error in %s", closer.__qualname__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
        root_path=settings.ROOT_PATH,
        debug=settings.DEBUG,
        lifespan=lifespan,
    )

    # Auth-exempt: Cloud Run probes hit /health unauthenticated.
    app.include_router(health.router)
    # Foods is global (cached OFF data, shared across users) — auth-gated only.
    app.include_router(foods.router)

    # Everything user-scoped lives under /users/{user_id}/... so the path itself
    # carries the identity claim. `owned_user_id` is mounted on the parent
    # router so every nested route inherits the 401/403 guard.
    users_router = APIRouter(
        prefix="/users/{user_id}",
        dependencies=[Depends(owned_user_id)],
    )
    users_router.include_router(journal.router)
    users_router.include_router(recipe.router)
    app.include_router(user.router)  # /users/{user_id} (top-level GET/PATCH)
    app.include_router(users_router)

    @app.exception_handler(EnvelopeHTTPException)
    async def _envelope_http_exc_handler(
        request: Request, exc: EnvelopeHTTPException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=ApiErrorResponse(
                error=ApiError(code=exc.code, message=str(exc.detail))
            ).model_dump(by_alias=True),
        )

    @app.exception_handler(HTTPException)
    async def _http_exc_handler(request: Request, exc: HTTPException) -> JSONResponse:
        # Catches any raw HTTPException (e.g. FastAPI internals). Converts to
        # the project's envelope so iOS / OpenAPI consumers see a uniform shape.
        return JSONResponse(
            status_code=exc.status_code,
            content=ApiErrorResponse(
                error=ApiError(code="HTTP_ERROR", message=str(exc.detail))
            ).model_dump(by_alias=True),
        )

    logger.info(
        "FastAPI application created: %s v%s (root_path=%s)",
        settings.APP_NAME,
        settings.APP_VERSION,
        settings.ROOT_PATH,
    )
    return app
