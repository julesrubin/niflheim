# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Personal cloud-native hosting platform for **https://www.julesrubin.com**. Caddy reverse proxy fronts a React portfolio and a FastAPI service, all on Cloud Run, deployed via Terraform + Cloud Build. Personal/PoC tone — ship fast, iterate.

Service-specific guidance lives in:
- `frontend/portfolio/CLAUDE.md` — React 18 + Tailwind + Framer Motion
- `backend/api/CLAUDE.md` — FastAPI + uv
- `backend/macrow/CLAUDE.md` — FastAPI + uv (food tracking)
- `backend/proxy/CLAUDE.md` — Caddy

## Request flow & path-prefix invariants

```
client → Caddy (/) → portfolio (/portfolio/*)
                   → api       (/api/*)
                   → macrow    (/macrow/*)
                   → 301 /  → /portfolio
                   → 200 /health
```

The path prefix is wired in **three coupled places** — touching one without the others breaks routing:

| Service   | Where it's set                                              |
|-----------|-------------------------------------------------------------|
| Caddy     | `backend/proxy/Caddyfile` — `handle_path /api/*`, `handle_path /macrow/*`, `handle_path /portfolio/*` (strips prefix before forwarding) |
| API       | `backend/api/src/api/main.py` — `FastAPI(root_path="/api")` |
| Macrow    | `backend/macrow/src/macrow/main.py` — `FastAPI(root_path="/macrow")` |
| Portfolio | `frontend/portfolio/package.json` `homepage: "/portfolio"` + `<BrowserRouter basename="/portfolio">` in `src/App.js` |

Caddy strips the prefix, so upstream services see clean paths and rebuild URLs from `root_path` / `basename`. If you add a new service, mirror this pattern.

## Build system

Just is the canonical task runner. Service justfiles are imported as namespaces from the root `justfile`:

- `portfolio::*` → `frontend/portfolio/justfile`
- `api::*`       → `backend/api/justfile`
- `macrow::*`    → `backend/macrow/justfile`
- `proxy::*`     → `backend/proxy/justfile`
- `infra::*`     → `gcp/justfile`

Useful entry points:
- `just --list` — discover recipes (don't memorize them)
- `just check-tools` — verify docker / terraform / gcloud / yarn / uv / node are installed
- `just infra::plan <service>` — Terraform plan for one service (`portfolio`, `api`, `proxy`, or empty for root)
- `just <ns>::image` and `just <ns>::push` — build/push a single service image

GCP project is hard-coded as `portfolio-jrubin` (region `europe-west1`) in the root and `gcp/` justfiles — single source of truth, change there if forking.

## CI/CD (Cloud Build)

`cloudbuild.yaml` defines a 4-step pipeline reused for every service:

1. **Project Init** — runs `scripts/init.sh ${_PROJECT_ID} ${_SUBFOLDER}`
2. **Docker Build & Push** — iterates `${_DOCKER_FOLDERS}` (comma-separated), tags as `${_REGION}-docker.pkg.dev/${_PROJECT_ID}/${_ARTIFACT_REGISTRY}/${_CONTEXT}:${SHORT_SHA}`
3. **Terraform Init & Plan** — `cd ${_SUBFOLDER}`, then plan with `-var="image_tag_suffix=${SHORT_SHA}"`
4. **Terraform Apply** — gated by `${_APPLY_CHANGES} == "true"` (otherwise dry-run)

Key substitutions per trigger: `_SUBFOLDER` (Terraform dir), `_DOCKER_FOLDERS` (which images to build), `_ARTIFACT_REGISTRY`, `_CONTEXT`, `_APPLY_CHANGES`. `SHORT_SHA` ties image tag and Terraform plan together — same SHA flows into both.

## Terraform layout

- `gcp/` — root infrastructure (project-wide resources)
- `gcp/services/{api,portfolio,proxy}/` — per-service Cloud Run + IAM + registry
- `gcp/modules/` — reusable modules
- Every service uses `init/backend.tfvars` for backend config and `config/variable.tfvars` for inputs (matches Cloud Build expectations)

## First-time GCP setup (non-obvious bits)

```bash
gcloud auth login && gcloud auth application-default login
gcloud config set project portfolio-jrubin
gcloud auth configure-docker europe-west1-docker.pkg.dev
```

Terraform state buckets and Artifact Registries must already exist before the first Cloud Build run — `scripts/init.sh` handles bootstrap when wired in.
