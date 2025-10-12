#!/usr/bin/env -S just --justfile
# Niflheim - Cloud-Native Hosting Platform

# GCP Configuration
GCP_PROJECT := "sandbox-jrubin"
GCP_REGION := "europe-west1"
ARTIFACT_REGISTRY_PORTFOLIO := "sandbox-jrubin-gcr-niflheim-portfolio"
ARTIFACT_REGISTRY_PROXY := "sandbox-jrubin-gcr-niflheim-proxy"
ARTIFACT_REGISTRY_API := "sandbox-jrubin-gcr-niflheim-api"

# Import service justfiles with namespaces
mod portfolio 'frontend/portfolio/justfile'
mod api 'backend/api/justfile'
mod proxy 'backend/proxy/justfile'
mod infra 'gcp/justfile'

# Default recipe - show available commands
[group('help')]
default:
    @just --list

# Show detailed help with all imported modules
[group('help')]
help:
    @echo "Niflheim Build System"
    @echo "====================="
    @echo ""
    @echo "Available command groups:"
    @echo "  - portfolio::*  Frontend portfolio commands"
    @echo "  - api::*        Backend API commands"
    @echo "  - proxy::*      Proxy service commands"
    @echo "  - infra::*      Infrastructure (Terraform) commands"
    @echo ""
    @echo "Root commands:"
    @just --list

# Build all Docker images
[group('docker')]
build-all-images:
    @echo "Building all Docker images..."
    cd {{ source_directory() }} && just portfolio::image
    cd {{ source_directory() }} && just api::image
    cd {{ source_directory() }} && just proxy::image

# Push all Docker images to GCP Artifact Registry
[group('docker')]
push-all-images:
    @echo "Pushing all Docker images..."
    cd {{ source_directory() }} && just portfolio::push
    cd {{ source_directory() }} && just api::push
    cd {{ source_directory() }} && just proxy::push

# Run all quality checks across services
[group('quality')]
quality-all:
    @echo "Running quality checks on all services..."
    cd {{ source_directory() }} && just portfolio::test
    cd {{ source_directory() }} && just api::lint
    cd {{ source_directory() }} && just api::test

# Initialize all Terraform services
[group('infra')]
tf-init-all:
    @echo "Initializing all Terraform services..."
    cd {{ source_directory() }} && just infra::init
    cd {{ source_directory() }} && just infra::init portfolio
    cd {{ source_directory() }} && just infra::init api
    cd {{ source_directory() }} && just infra::init proxy

# Plan all Terraform services
[group('infra')]
tf-plan-all:
    @echo "Planning all Terraform services..."
    cd {{ source_directory() }} && just infra::plan
    cd {{ source_directory() }} && just infra::plan portfolio
    cd {{ source_directory() }} && just infra::plan api
    cd {{ source_directory() }} && just infra::plan proxy

# Clean all build artifacts
[group('maintenance')]
clean:
    #!/usr/bin/env bash
    cd {{ source_directory() }}
    echo "Cleaning build artifacts..."
    rm -rf frontend/portfolio/build
    rm -rf frontend/portfolio/node_modules
    rm -rf backend/api/.venv
    find . -name "*.tfplan" -type f -delete
    find . -name ".terraform" -type d -exec rm -rf {} + 2>/dev/null || true
    echo "Clean complete!"

# Check if required tools are installed
[group('setup')]
check-tools:
    #!/usr/bin/env bash
    cd {{ source_directory() }}
    echo "Checking required tools..."

    tools=("docker" "terraform" "gcloud" "yarn" "uv" "node")
    missing=()

    for tool in "${tools[@]}"; do
        if command -v "$tool" &> /dev/null; then
            echo "✓ $tool installed"
        else
            echo "✗ $tool NOT FOUND"
            missing+=("$tool")
        fi
    done

    if [ ${#missing[@]} -gt 0 ]; then
        echo ""
        echo "Missing tools: ${missing[*]}"
        exit 1
    fi

    echo ""
    echo "All required tools are installed!"
