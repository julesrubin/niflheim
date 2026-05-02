"""FastAPI application factory."""

import logging

from fastapi import FastAPI

from .config.settings import settings
from .routes import foods, health

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
        root_path=settings.ROOT_PATH,
        debug=settings.DEBUG,
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
