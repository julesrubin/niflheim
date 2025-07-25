locals {
  substitutions = {
    _PROJECT_ID        = var.project_id
    _REGION            = var.region
    _ARTIFACT_REGISTRY = google_artifact_registry_repository.cloud_run_images.name

  }
}

locals {
  applications = {
    core = {
      included_files = ["gcp/**"]
      ignored_files  = ["gcp/services/**"]
      substitutions = {
        _SUBFOLDER      = "gcp"
        _DOCKER_FOLDERS = ""
      }
    },
    proxy = {
      included_files = ["gcp/services/proxy/**", "backend/proxy/**"]
      ignored_files  = []
      substitutions = {
        _SUBFOLDER      = "gcp/services/proxy"
        _DOCKER_FOLDERS = "backend/proxy"
      }
    },
    portfolio = {
      included_files = ["gcp/services/portfolio/**", "frontend/portfolio/**"]
      ignored_files  = []
      substitutions = {
        _SUBFOLDER      = "gcp/services/portfolio"
        _DOCKER_FOLDERS = "frontend/portfolio"
      }
    }
  }

  # Define a map for plan trigger configurations
  plan_triggers = {
    for key, app in local.applications : key => {
      name           = "${var.repository_name}-${key}-tf-plan"
      included_files = app.included_files
      ignored_files  = app.ignored_files
      substitutions = merge(
        local.substitutions,
        app.substitutions,
        {
          _APPLY_CHANGES = "false",
          _CONTEXT       = key
        }
      )
    }
  }
  # Define a map for apply trigger configurations
  apply_triggers = {
    for key, app in local.applications : key => {
      name           = "${var.repository_name}-${key}-tf-apply"
      included_files = app.included_files
      ignored_files  = app.ignored_files
      substitutions = merge(
        local.substitutions,
        app.substitutions,
        {
          _APPLY_CHANGES = "true",
          _CONTEXT       = key
        }
      )
    }
  }
}

resource "google_cloudbuild_trigger" "tf_plan" {
  for_each = local.plan_triggers

  project         = var.project_id
  name            = each.value.name
  location        = var.region
  filename        = "cloudbuild.yaml"
  service_account = google_service_account.service_account["cloud-build-deploy"].id
  included_files  = each.value.included_files
  ignored_files   = each.value.ignored_files
  substitutions   = each.value.substitutions

  repository_event_config {
    repository = google_cloudbuildv2_repository.github_repo.id
    pull_request {
      branch = "^main"
    }
  }
}

resource "google_cloudbuild_trigger" "tf_apply" {
  for_each = local.apply_triggers

  project         = var.project_id
  name            = each.value.name
  location        = var.region
  filename        = "cloudbuild.yaml"
  service_account = google_service_account.service_account["cloud-build-deploy"].id
  included_files  = each.value.included_files
  ignored_files   = each.value.ignored_files
  substitutions   = each.value.substitutions

  repository_event_config {
    repository = google_cloudbuildv2_repository.github_repo.id

    push {
      branch = "^main"
    }
  }
}
