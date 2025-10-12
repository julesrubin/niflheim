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
├── Makefile                    # Build, deploy, and infrastructure commands
└── cloudbuild.yaml             # GCP Cloud Build CI/CD configuration
```

## Common Development Commands

### Local Development

**Frontend (Portfolio)**:
```bash
cd frontend/portfolio
yarn install
yarn start                      # Dev server on localhost:3000
yarn test                       # Run tests
yarn build                      # Production build
```

**Backend (API)**:
```bash
cd backend/api
uv sync --active                # Install dependencies with uv
uv run uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
# API available at http://localhost:8000/api/
```

**Proxy (Local Testing)**:
```bash
cd backend/proxy
docker build -t niflheim-proxy .
docker run -p 8080:8080 \
  -e PORT=8080 \
  -e API_SERVICE_URL=http://host.docker.internal:8000 \
  -e PORTFOLIO_SERVICE_URL=http://host.docker.internal:3000 \
  niflheim-proxy
```

### Docker Operations

**Build images** (from repository root):
```bash
make image portfolio            # Build portfolio Docker image
make image proxy                # Build proxy Docker image
```

**Run containers locally**:
```bash
make run portfolio              # Run portfolio on port 8080
make run proxy                  # Run proxy on port 8080
```

**Push to GCP Artifact Registry**:
```bash
make push portfolio
make push proxy
```

**Deploy to Cloud Run**:
```bash
make deploy portfolio
make deploy proxy
```

**All-in-one deployment** (build + push + deploy):
```bash
make all-portfolio
make all-proxy
```

### Infrastructure Management (Terraform)

**Initialize Terraform** (required first time or after backend changes):
```bash
make init                       # Initialize root gcp/ directory
make init portfolio             # Initialize specific service
make init proxy
```

**Plan infrastructure changes**:
```bash
make plan                       # Plan root infrastructure
make plan portfolio             # Plan portfolio service
make plan proxy                 # Plan proxy service
```

**Apply infrastructure changes**:
```bash
make apply                      # Apply planned changes
```

Note: `make plan` automatically runs `make init`, so you can typically skip the init step.

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
- **Node.js**: v18+ (frontend)
- **Python**: 3.13+ (backend - enforced via .python-version)
- **uv**: Python package manager for backend
- **Docker**: Container builds and local testing
- **Terraform**: v1.8.0+ (infrastructure management)
- **Google Cloud SDK**: For GCP deployment (`gcloud` CLI)
- **Yarn**: Frontend package manager

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

## Contributing

When adding new services:
1. Create service directory in appropriate location (frontend/backend)
2. Add Dockerfile for containerization
3. Create Terraform configuration in `gcp/services/<service>`
4. Update Caddyfile with new routing rules
5. Add Makefile targets for build/deploy operations
6. Create service-specific CLAUDE.md documenting architecture
7. Update root CLAUDE.md with integration points
