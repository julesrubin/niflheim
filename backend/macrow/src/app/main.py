"""Application entry point. uvicorn target = `src.app.main:app`."""

from .application import create_app
from .utils.logger import config_logger

config_logger()
app = create_app()
