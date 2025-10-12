# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Niflheim is a cloud-native hosting platform deployed on Google Cloud Platform (GCP) that serves as a unified entry point for multiple services through intelligent routing. The platform consists of a React portfolio frontend, a FastAPI backend, and a Caddy reverse proxy, all containerized and deployed on GCP Cloud Run with Terraform-managed infrastructure.

**Live Site**: https://www.julesrubin.com

**Architecture**: Microservices architecture with Caddy proxy routing to multiple backend services
- Frontend (React portfolio) → `/portfolio` path
- Backend API (FastAPI) → `/api` path
- Reverse proxy (Caddy) → Entry point handling routing and redirects

## Repository Structure

```
niflheim/
├── frontend/portfolio/          # React portfolio (see portfolio/CLAUDE.md)
├── backend/
│   ├── api/                    # FastAPI backend (see api/CLAUDE.md)
│   └── proxy/                  # Caddy reverse proxy (see proxy/CLAUDE.md)
├── gcp/                        # Terraform infrastructure as code
│   ├── services/               # Service-specific Terraform configs
│   └── modules/                # Reusable Terraform modules
├── scripts/                    # Deployment and utility scripts
├── justfile                    # Root build system (Just task runner)
└── cloudbuild.yaml             # GCP Cloud Build CI/CD configuration
```

## Build System

Niflheim uses **Just** (a modern command runner) instead of Make for all build, deployment, and infrastructure commands. Each service has its own justfile with service-specific commands, and the root justfile imports all service justfiles with namespaces.

**Why Just over Make:**
- Modular service-specific justfiles with imports
- Better parameter handling and typed arguments
- Cross-platform consistency
- Built-in recipe documentation with groups
- Can run commands from any directory using `source_directory()`

### Quick Start

```bash
# Install Just: https://github.com/casey/just
# macOS: brew install just
# Linux: cargo install just

# Show all available commands
just --list

# Show detailed help
just help

# Check required tools are installed
just check-tools
```

## Common Development Commands

All commands use the `just` task runner. You can run them from any directory in the repository.

### Local Development

**Portfolio (Frontend)**:
```bash
# From root directory or frontend/portfolio:
just portfolio::install         # Install dependencies with Yarn
just portfolio::start           # Dev server on localhost:3000
just portfolio::test            # Run tests
just portfolio::build           # Production build
just portfolio::build-css       # Build TailwindCSS
```

**API (Backend)**:
```bash
# From root directory or backend/api:
just api::install               # Install dependencies with UV
just api::run                   # Run API server locally (port 8000)
just api::serve                 # Run with custom host/port
just api::format                # Format code with ruff
just api::lint                  # Lint code with ruff
just api::test                  # Run tests with coverage
just api::pre-commit            # Run all quality checks
```

**Proxy**:
```bash
# From root directory or backend/proxy:
just proxy::image               # Build Docker image
just proxy::run                 # Run locally (default config)
just proxy::run-custom 8080 http://api:8000 http://portfolio:3000
just proxy::health              # Test health endpoint
just proxy::test-routes         # Test all routing rules
just proxy::validate            # Validate Caddyfile (if Caddy installed)
```

### Docker Operations

**Build images**:
```bash
just portfolio::image           # Build portfolio Docker image
just api::image                 # Build API Docker image
just proxy::image               # Build proxy Docker image
just build-all-images           # Build all images
```

**Push to GCP Artifact Registry**:
```bash
just portfolio::push            # Push portfolio image
just api::push                  # Push API image
just proxy::push                # Push proxy image
just push-all-images            # Push all images
```

**Run containers locally**:
```bash
just portfolio::run             # Run portfolio on port 8080
just api::run-container         # Run API on port 8000
just proxy::run                 # Run proxy on port 8080
```

**Deploy to Cloud Run** (DANGEROUS - requires GCP credentials):
```bash
just portfolio::deploy          # Deploy portfolio
just api::deploy                # Deploy API
just proxy::deploy              # Deploy proxy
```

**All-in-one deployment** (build + push + deploy):
```bash
just portfolio::all             # Portfolio: image → push → deploy
just api::all                   # API: image → push → deploy
just proxy::all                 # Proxy: image → push → deploy
```

### Infrastructure Management (Terraform)

**Terraform commands** (via infra module):
```bash
# Initialize Terraform
just infra::init                # Initialize root infrastructure
just infra::init portfolio      # Initialize portfolio service
just infra::init api            # Initialize API service
just infra::init proxy          # Initialize proxy service
just tf-init-all                # Initialize all services

# Plan changes
just infra::plan                # Plan root infrastructure
just infra::plan portfolio      # Plan portfolio service
just infra::plan api            # Plan API service
just infra::plan proxy          # Plan proxy service
just tf-plan-all                # Plan all services

# Apply changes (DANGEROUS)
just infra::apply               # Apply root infrastructure
just infra::apply portfolio     # Apply portfolio service

# Other Terraform commands
just infra::validate            # Validate configuration
just infra::format              # Format Terraform files
just infra::output              # Show outputs
just infra::state               # Show state
just infra::destroy portfolio   # Destroy service (prompts confirmation)
```

Note: `just infra::plan` automatically runs `init` as a dependency.

## High-Level Architecture

### Request Flow
```
User → Caddy Proxy (GCP Cloud Run)
       ├─ / → 301 redirect to /portfolio
       ├─ /health → 200 OK health check
       ├─ /api/* → FastAPI Backend (GCP Cloud Run)
       └─ /portfolio/* → React Frontend (GCP Cloud Run)
```

### Service Communication
- **Proxy Service**: Entry point receiving all external traffic, routes based on path prefixes
- **API Service**: FastAPI backend with `/api` root_path, handles backend logic
- **Portfolio Service**: React SPA served via nginx, runs at `/portfolio` base path

### GCP Infrastructure (Terraform-Managed)
- **Cloud Run**: Serverless container platform for all services
- **Artifact Registry**: Container image storage (separate registries per service)
- **Cloud Build**: CI/CD with GitHub integration (2ndGen connection required)
- **IAM**: Service accounts and roles for secure inter-service communication
- **Cloud Storage**: Terraform state management (GCS backend)

### CI/CD Pipeline (cloudbuild.yaml)
1. **Project Init**: Initialize service with scripts/init.sh
2. **Docker Build/Push**: Build images and push to Artifact Registry (if `_DOCKER_FOLDERS` set)
3. **Terraform Init**: Initialize with GCS backend
4. **Terraform Plan**: Plan infrastructure changes with dynamic image tags (SHORT_SHA)
5. **Terraform Apply**: Apply changes (controlled by `_APPLY_CHANGES` flag)

## Deployment Architecture

### Service Configuration Pattern
Each service (portfolio, api, proxy) has its own Terraform configuration in `gcp/services/<service>/`:
- `config/variable.tfvars` - Service-specific variables (project_id, region, etc.)
- `init/backend.tfvars` - GCS backend configuration for Terraform state
- `main.tf` - Service infrastructure definition

### Image Naming Convention
Images are tagged with Git SHA for version tracking:
```
<region>-docker.pkg.dev/<project>/<artifact-registry>/<context>:<SHORT_SHA>
```

### Environment-Specific Configuration
- **Development**: Local Docker containers with port forwarding
- **Production**: GCP Cloud Run with managed HTTPS, auto-scaling, and IAM authentication

## Key Integration Points

### Portfolio Base Path Configuration
The portfolio React app runs at `/portfolio` base path:
- `package.json`: `"homepage": "/portfolio"`
- `App.js`: `<BrowserRouter basename="/portfolio">`
- nginx.conf: Handles SPA routing with try_files fallback

### API Root Path Configuration
The FastAPI app uses `root_path="/api"`:
- `main.py`: `FastAPI(root_path="/api")`
- All routes automatically prefixed with `/api`
- Important for proxy integration and OpenAPI docs

### Proxy Routing Logic (Caddyfile)
- Uses `handle_path` directive to strip path prefixes before forwarding
- Sets `X-Forwarded-Proto: https` header
- Updates `Host` header to upstream target
- Health check endpoint bypasses proxy logic

## Prerequisites for Development

### Required Software
- **Just**: Command runner - `brew install just` (macOS) or see https://github.com/casey/just
- **Node.js**: v18+ (frontend)
- **Python**: 3.13+ (backend - enforced via .python-version)
- **uv**: Python package manager for backend - https://docs.astral.sh/uv/
- **Docker**: Container builds and local testing
- **Terraform**: v1.8.0+ (infrastructure management)
- **Google Cloud SDK**: For GCP deployment (`gcloud` CLI)
- **Yarn**: Frontend package manager

Run `just check-tools` to verify all required tools are installed.

### GCP Setup (First-Time Deployment)
1. Enable required GCP APIs:
   ```bash
   gcloud services enable cloudbuild.googleapis.com \
       artifactregistry.googleapis.com \
       run.googleapis.com \
       secretmanager.googleapis.com \
       cloudresourcemanager.googleapis.com \
       --project=<PROJECT_ID>
   ```

2. Run initialization script for each service:
   ```bash
   ./scripts/init.sh <PROJECT_ID> <service_folder>
   # Example: ./scripts/init.sh my-project gcp/services/portfolio
   ```

3. Configure GitHub 2ndGen connection in GCP Console:
   - Connection must be named `github_connection`
   - Or update the name in `gcp/repo_connection.tf`

## Service-Specific Documentation

Each service has its own detailed CLAUDE.md file:

- **Portfolio (React)**: `frontend/portfolio/CLAUDE.md`
  - Component organization, routing, dark mode, project data structure
  - TailwindCSS styling conventions, Framer Motion animations
  - EmailJS integration, adding new projects

- **API (FastAPI)**: `backend/api/CLAUDE.md`
  - Router-based architecture, adding endpoints
  - Root path configuration, dependency management with uv
  - Docker configuration

- **Proxy (Caddy)**: `backend/proxy/CLAUDE.md`
  - Routing configuration, environment variables
  - Testing proxy routes, making configuration changes

## Testing

**Portfolio Tests**:
```bash
cd frontend/portfolio
yarn test
# Tests: Banner.test.js, Modal.test.js (React Testing Library)
```

**API Tests**:
Currently no test suite configured - tests would use pytest/FastAPI TestClient.

**Integration Testing**:
Use proxy health checks and manual routing verification:
```bash
curl http://localhost:8080/health
curl http://localhost:8080/api/
curl http://localhost:8080/portfolio
```

## Troubleshooting

### Docker Build Issues
- Ensure using `--platform linux/amd64` for GCP Cloud Run compatibility
- Check Dockerfile paths relative to build context (service directory)

### Terraform State Issues
- Verify GCS backend bucket exists and you have access
- Check `init/backend.tfvars` configuration matches GCS setup
- Use `terraform init -reconfigure` to reinitialize backend

### Cloud Build Failures
- Verify `_APPLY_CHANGES` substitution variable (true/false)
- Check `_SUBFOLDER` points to correct service directory
- Ensure GitHub 2ndGen connection is configured

### Local Proxy Testing
- Use `host.docker.internal` for Docker to access host services
- Verify environment variables are set correctly
- Check Caddy logs for routing issues

## Maintenance Commands

```bash
# Clean all build artifacts
just clean                      # Root-level clean (all services)
just portfolio::clean           # Clean portfolio artifacts
just api::clean                 # Clean API artifacts
just infra::clean               # Clean Terraform artifacts

# Run quality checks across all services
just quality-all                # Run tests and linting for all services
```

## Justfile Architecture

The repository uses a modular justfile structure with imports:

```
justfile                        # Root orchestrator, imports all service justfiles
├── frontend/portfolio/justfile # Portfolio-specific commands
├── backend/api/justfile        # API-specific commands
├── backend/proxy/justfile      # Proxy-specific commands
└── gcp/justfile                # Infrastructure commands
```

**Key features:**
- Each service justfile can be run independently from its directory
- Root justfile imports service justfiles with namespaces (portfolio::, api::, proxy::, infra::)
- All commands use `cd {{ source_directory() }}` to support execution from any directory
- Commands are organized into groups for better discovery (`just --list`)
- GCP configuration (project, region, registries) defined at root level

## Contributing

When adding new services:
1. Create service directory in appropriate location (frontend/backend)
2. Add Dockerfile for containerization
3. Create service-specific `justfile` with standard recipe groups:
   - `[setup]`: Install dependencies
   - `[dev]`: Development commands (start, run)
   - `[quality]`: Format, lint, test
   - `[docker]`: image, push, run
   - `[deploy]`: deploy, all
   - `[maintenance]`: clean
4. Import new justfile in root justfile: `mod <name> '<path>/justfile'`
5. Create Terraform configuration in `gcp/services/<service>`
6. Update Caddyfile with new routing rules
7. Create service-specific CLAUDE.md documenting architecture
8. Update root CLAUDE.md with integration points
