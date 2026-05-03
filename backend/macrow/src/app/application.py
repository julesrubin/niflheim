"""FastAPI application factory."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .config.settings import settings
from .routes import foods, health
from .services.food import FoodRepository
from .services.off import OffClient

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
    logger.info(
        "Lifespan ready: OFF=%s firestore=%s/%s",
        settings.OFF_BASE_URL,
        settings.FIRESTORE_PROJECT or "<adc-default>",
        settings.FIRESTORE_DATABASE,
    )
    try:
        yield
    finally:
        await app.state.off_client.aclose()
        app.state.food_repo.close()


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

    app.include_router(health.router)
    app.include_router(foods.router)

    logger.info(
        "FastAPI application created: %s v%s (root_path=%s)",
        settings.APP_NAME,
        settings.APP_VERSION,
        settings.ROOT_PATH,
    )
    return app
