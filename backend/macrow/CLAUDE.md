# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Macrow is a personal food-tracking FastAPI service for the Niflheim platform. Containerized with Docker, Python 3.13, `uv` for dependency management. Runs on Cloud Run behind the shared Caddy proxy at `/macrow/*`.

## Development Commands

```bash
# Install / sync deps (uv is the package manager — never edit pyproject.toml deps directly)
just install            # = uv sync --active
uv add <package>        # add a runtime dep
uv add --dev <package>  # add a dev dep

# Run locally
just run                # uvicorn with --reload on :8000

# Quality
just lint               # ruff check
just format             # ruff format
just test               # pytest --cov=src/app
just pre-commit         # format + lint + test

# Docker / GCP
just image              # build linux/amd64 image
just push               # push to Artifact Registry
just deploy             # gcloud run deploy
```

### API access

- Local base URL: `http://localhost:8000`
- All routes are prefixed with `/macrow` (`root_path` in `application.py`, sourced from `Settings.ROOT_PATH`).
- In production, Caddy strips `/macrow/` before forwarding; upstream code rebuilds URLs from `root_path`.

## Architecture

### Source layout

```
src/app/
├── main.py              # uvicorn entrypoint: configures logging, calls create_app()
├── application.py       # FastAPI factory — registers routers, sets metadata from settings
├── config/
│   ├── settings.py      # pydantic-settings BaseSettings (env + .env)
│   └── constants.py     # non-environment constants (search bounds, etc.)
├── models/              # Pydantic DTOs (request/response shapes)
│   ├── common.py        # CamelModel base, ApiError envelope, shared enums
│   └── food.py          # Food, FoodSearchResponse, SourceBreakdown
├── routes/              # FastAPI APIRouter modules (one per resource)
│   ├── health.py        # GET /health
│   └── foods.py         # GET /foods/{barcode}, GET /foods/search
├── services/            # Business logic (OFF client, cache ops — populated in step 7)
├── middleware/          # Custom ASGI middleware (CORS, etc. — empty for now)
└── utils/
    ├── error.py         # error_response(), not_implemented(), barcode_not_found(), …
    └── logger.py        # config_logger() — single stream handler, level from settings
```

The package is named `macrow` in `pyproject.toml` but the import root is `app` (configured via `[tool.hatch.build.targets.wheel] packages = ["src/app"]`). uvicorn target: `src.app.main:app`.

### Conventions

- **Wire format is camelCase.** Every model inherits from `models.common.CamelModel`, which sets `populate_by_name=True` and `alias_generator=to_camel`. Python keeps snake_case; JSON sees camelCase. Matches Swift `Codable` defaults on the iOS client.
- **Error envelope is uniform.** All non-2xx responses use `{ "error": { "code", "message", "details"? } }`. Build them via helpers in `utils/error.py` — never `raise HTTPException` with a free-form string.
- **Error codes are SCREAMING_SNAKE.** e.g. `BARCODE_NOT_FOUND`, `OFF_UNAVAILABLE`, `NOT_IMPLEMENTED`.
- **Settings come from env via `pydantic-settings`.** Don't hardcode hosts, timeouts, log levels, or `root_path` — add a field to `config/settings.py`.
- **Constants are not env-driven.** Search bounds, default limits, etc. go in `config/constants.py`.

### Adding a new endpoint

1. Add the DTOs to `models/<resource>.py` (inherit `CamelModel`).
2. Create `routes/<resource>.py`:
   ```python
   router = APIRouter(prefix="/<resource>", tags=["<resource>"])

   @router.get("/...", response_model=...)
   async def handler(...): ...
   ```
3. Register in `application.py`: `from .routes import <resource>` then `app.include_router(<resource>.router)`.
4. If you need a non-success response, return one of the helpers in `utils/error.py` (or add a new one there — keep it shared).
5. Reachable at `http://localhost:8000/macrow/<route-path>`.

### Path-prefix invariant

`root_path="/macrow"` in `application.py` must stay in sync with the Caddy `handle_path /macrow*` block in `backend/proxy/Caddyfile`. Caddy strips the prefix before forwarding; FastAPI re-prepends it via `root_path` so OpenAPI URLs match what clients see externally.

## Technology stack

- **Python**: 3.13 (enforced via `.python-version`)
- **Framework**: FastAPI 0.116+
- **Validation**: Pydantic v2 + pydantic-settings
- **Server**: Uvicorn
- **Package manager**: `uv`
- **Container**: Docker, `python:3.13-slim` base

## Docker

`Dockerfile` is layer-cache-friendly: install `uv`, copy `pyproject.toml` + `uv.lock`, install deps, then copy `src/`. Runs `uvicorn src.app.main:app --host 0.0.0.0 --port 8000`. Image is published to GCP Artifact Registry by `just push` and deployed to Cloud Run by `just deploy`.
