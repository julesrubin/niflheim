"""Logging configuration."""

import logging

from ..config.settings import settings


def config_logger() -> None:
    """Configure root logger with a single stream handler at the configured level."""
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(levelname)-8s %(name)s: %(message)s"),
    )
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        handlers=[handler],
        force=True,
    )
