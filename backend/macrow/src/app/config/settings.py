"""Application configuration using Pydantic BaseSettings."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings loaded from env vars + .env, with typed defaults."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    APP_NAME: str = Field(default="Macrow")
    APP_DESCRIPTION: str = Field(default="Personal food tracking service.")
    APP_VERSION: str = Field(default="0.1.0")
    ROOT_PATH: str = Field(default="/macrow")

    DEBUG: bool = Field(default=False)
    LOG_LEVEL: str = Field(default="INFO")

    OFF_BASE_URL: str = Field(default="https://world.openfoodfacts.org")
    OFF_TIMEOUT_SECONDS: float = Field(default=5.0)


settings = Settings()
