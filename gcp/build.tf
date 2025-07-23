locals {
  substitutions = {
    _PROJECT_ID = var.project_id
    _REGION     = var.region
  }
}

locals {
  applications = {
    root = {
      included_files = ["gcp/**"]
      ignored_files  = ["gcp/apis/**", "gcp/portfolio/**"]
      substitutions = {
        _SUBFOLDER      = "gcp"
        _DOCKER_FOLDERS = ""
      }
    },
    # portfolio = {
    #   included_files = ["gcp/portfolio/**", "frontend/portfolio/**"]
    #   ignored_files  = []
    #   substitutions = {
    #     _SUBFOLDER         = "gcp/portfolio"
    #     _DOCKER_FOLDERS    = "frontend/portfolio"
    #     _ARTIFACT_REGISTRY = "sandbox-jrubin-gcr-niflheim-portfolio"
    #   }
    # },
    # apis = {
    #   included_files = ["gcp/apis/**"]
    #   ignored_files  = []
    #   substitutions = {
    #     _SUBFOLDER      = "gcp/apis"
    #     _DOCKER_FOLDERS = ""
    #   }
    # }
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
    pull_request {
      branch = "^main"
    }
  }
}
