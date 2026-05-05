"""Application configuration using Pydantic BaseSettings."""

from pydantic import Field, SecretStr
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
    # search-a-licious is OFF's Elasticsearch-backed free-text endpoint, on a
    # separate host. v2 /api/search is filter-only and v1 cgi/search.pl is
    # legacy MongoDB scan — search-a-licious is the modern path.
    OFF_SEARCH_BASE_URL: str = Field(default="https://search.openfoodfacts.org")
    OFF_TIMEOUT_SECONDS: float = Field(default=5.0)
    OFF_USER_AGENT: str = Field(default="Macrow/0.1.0 (https://julesrubin.com/macrow)")

    FIRESTORE_PROJECT: str | None = Field(default=None)
    FIRESTORE_DATABASE: str = Field(default="macrow")

    # Single shared secret for the bearer-token guard. Provisioned out-of-band
    # via Secret Manager (`niflheim-macrow-bearer-token`) and mounted into the
    # Cloud Run env as BEARER_TOKEN. No default — startup fails loud if missing.
    BEARER_TOKEN: SecretStr
    # Today the bearer token resolves to this single user id. When auth grows
    # to Firebase, the auth module returns the verified `uid` claim instead.
    CURRENT_USER_ID: str = Field(default="me")


settings = Settings()
