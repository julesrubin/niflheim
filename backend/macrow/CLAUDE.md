# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Macrow is a personal food-tracking FastAPI service for the Niflheim platform. Containerized with Docker, Python 3.13, `uv` for dependency management. Runs on Cloud Run behind the shared Caddy proxy at `/macrow/*`.

## Development Commands

### Dependency Management
```bash
# Install dependencies (uv is the package manager)
uv sync --active

# Add a new dependency (never edit pyproject.toml deps directly)
uv add <package-name>
```

### Running the Application
```bash
# Run locally (from this directory)
uv run uvicorn src.macrow.main:app --reload --host 0.0.0.0 --port 8000

# Run with Docker
docker build -t niflheim-macrow .
docker run -p 8000:8000 niflheim-macrow
```

### API Access
- Local base URL: `http://localhost:8000`
- All routes are prefixed with `/macrow` (configured via `root_path` in `main.py`)
- Root endpoint: `http://localhost:8000/macrow/`
- Example endpoint: `http://localhost:8000/macrow/items`

In production, Caddy strips `/macrow/` before forwarding, so upstream code rebuilds URLs from `root_path`.

## Architecture

### Application Structure
```
src/macrow/
├── main.py          # FastAPI app initialization, root_path configuration
├── routers/         # Route modules
│   └── items.py     # Example router with /items endpoint
└── __init__.py
```

### Key Architectural Patterns

**Router-Based Organization**: Uses FastAPI's `APIRouter` for modular routes. Each module in `src/macrow/routers/` defines a related set of endpoints.

**Root Path Configuration**: `FastAPI(root_path="/macrow")` (`main.py`) — must stay in sync with the Caddy `handle_path /macrow*` route in `backend/proxy/Caddyfile`.

**Router Registration**: Routers are explicitly included via `app.include_router()` in `main.py`. New routers must be wired the same way.

### Adding New Endpoints

1. Create a new router file in `src/macrow/routers/` (or extend an existing one)
2. `router = APIRouter()`
3. Add handlers with `@router.get()`, `@router.post()`, etc.
4. Import and include the router in `src/macrow/main.py`:
   ```python
   from .routers import new_router
   app.include_router(new_router.router)
   ```
5. Reachable at `http://localhost:8000/macrow/<route-path>`

## Technology Stack

- **Python**: 3.13 (enforced via `.python-version`)
- **Framework**: FastAPI 0.116.1+
- **Server**: Uvicorn 0.35.0+
- **Validation**: Pydantic 2.11.7+
- **Package Manager**: `uv`
- **Container**: Docker, `python:3.13-slim` base

## Docker Configuration

The Dockerfile is layer-cache-friendly:
1. Installs `uv`
2. Copies and installs dependencies first (`pyproject.toml`, `uv.lock`)
3. Copies source after dependencies
4. Exposes port 8000
5. Runs uvicorn with module path `src.macrow.main:app`
