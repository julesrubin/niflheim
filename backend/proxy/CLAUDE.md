# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Caddy-based reverse proxy service that routes traffic between the API and portfolio services in the Niflheim backend infrastructure.

## Architecture

**Proxy Pattern**: Caddy acts as the entry point for all HTTP traffic, routing requests based on path prefixes:
- `/api/*` → Routes to API service via `$API_SERVICE_URL`
- `/portfolio/*` → Routes to portfolio service via `$PORTFOLIO_SERVICE_URL`
- `/` → Redirects to `/portfolio` (301)
- `/health` → Returns 200 OK for health checks

**Configuration**: The `Caddyfile` defines all routing logic. It strips the path prefix before forwarding (using `handle_path`) and sets appropriate headers:
- `Host` header: Set to upstream host/port
- `X-Forwarded-Proto`: Set to `https` for all proxied requests

**Deployment**: Uses Caddy 2 Alpine Docker image. The Dockerfile simply copies the Caddyfile into the container.

## Environment Variables

Required for runtime configuration:
- `PORT` - Port Caddy listens on
- `API_SERVICE_URL` - Backend API service URL
- `PORTFOLIO_SERVICE_URL` - Backend portfolio service URL

## Docker Operations

**Build the image**:
```bash
docker build -t niflheim-proxy .
```

**Run locally** (example):
```bash
docker run -p 8080:8080 \
  -e PORT=8080 \
  -e API_SERVICE_URL=http://api:8000 \
  -e PORTFOLIO_SERVICE_URL=http://portfolio:3000 \
  niflheim-proxy
```

## Testing the Proxy

**Health check**:
```bash
curl http://localhost:8080/health
```

**Test routing**:
```bash
# Should redirect to /portfolio
curl -I http://localhost:8080/

# Test API routing (path prefix stripped)
curl http://localhost:8080/api/some-endpoint

# Test portfolio routing (path prefix stripped)
curl http://localhost:8080/portfolio/some-page
```

## Making Configuration Changes

When modifying the `Caddyfile`:
1. Edit the Caddyfile with your routing changes
2. Test locally with `caddy validate` if Caddy is installed, or rebuild the Docker image
3. Rebuild the Docker image to include changes
4. The `handle_path` directive automatically strips the path prefix before proxying
