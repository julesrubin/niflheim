# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastAPI-based backend API service for the Niflheim project. The API is containerized with Docker and uses Python 3.13 with `uv` as the package manager.

## Development Commands

### Dependency Management
```bash
# Install dependencies (uv is the package manager)
uv sync --active

# Add a new dependency
uv add <package-name>
# Then update pyproject.toml [project.dependencies] manually
```

### Running the Application
```bash
# Run locally (from repository root)
uv run uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# Run with Docker
docker build -t niflheim-api .
docker run -p 8000:8000 niflheim-api
```

### API Access
- Local base URL: `http://localhost:8000`
- All routes are prefixed with `/api` (configured via `root_path` in main.py:5)
- Root endpoint: `http://localhost:8000/api/`
- Example endpoint: `http://localhost:8000/api/items`

## Architecture

### Application Structure
```
src/api/
├── main.py          # FastAPI app initialization, root_path configuration
├── routers/         # API route modules
│   └── items.py     # Example router with /items endpoint
└── __init__.py
```

### Key Architectural Patterns

**Router-Based Organization**: The API uses FastAPI's APIRouter pattern for modular route organization. Each router module in `src/api/routers/` defines a collection of related endpoints.

**Root Path Configuration**: The FastAPI app is configured with `root_path="/api"` (main.py:5), meaning all routes are automatically prefixed with `/api`. This is important for proxy/gateway integration - when adding routes, they're accessed as `/api/<route>`.

**Router Registration**: Routers must be explicitly included in main.py using `app.include_router()` (main.py:9). New routers should follow this pattern.

### Adding New Endpoints

1. Create a new router file in `src/api/routers/` or use existing router
2. Define router: `router = APIRouter()`
3. Add route handlers with `@router.get()`, `@router.post()`, etc.
4. Import and include router in `src/api/main.py`:
   ```python
   from .routers import new_router
   app.include_router(new_router.router)
   ```
5. Access endpoint at: `http://localhost:8000/api/<route-path>`

## Technology Stack

- **Python**: 3.13 (enforced via .python-version)
- **Framework**: FastAPI 0.116.1+
- **Server**: Uvicorn 0.35.0+
- **Validation**: Pydantic 2.11.7+
- **Package Manager**: uv
- **Container**: Docker with python:3.13-slim base image

## Docker Configuration

The Dockerfile is optimized for layer caching:
1. Installs `uv` package manager
2. Copies and installs dependencies first (pyproject.toml, uv.lock)
3. Copies source code after dependencies
4. Exposes port 8000
5. Runs uvicorn server with module path `src.api.main:app`
