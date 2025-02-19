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
    portfolio = {
      included_files = ["gcp/portfolio/**", "frontend/portfolio/**"]
      ignored_files  = []
      substitutions = {
        _SUBFOLDER         = "gcp/portfolio"
        _DOCKER_FOLDERS    = "frontend/portfolio"
        _ARTIFACT_REGISTRY = "sandbox-jrubin-gcr-niflheim-portfolio"
      }
    },
    apis = {
      included_files = ["gcp/apis/**"]
      ignored_files  = []
      substitutions = {
        _SUBFOLDER      = "gcp/apis"
        _DOCKER_FOLDERS = ""
      }
    }
  }

  # Shared configurations
  plan_config = {
    name_suffix   = "tf-plan"
    event_type    = "pull_request"
    branch_regex  = "^main"
    apply_changes = "false" # Do not auto-apply
  }

  apply_config = {
    name_suffix   = "tf-apply"
    event_type    = "push"
    branch_regex  = "^main"
    apply_changes = "true" # Auto-apply after plan
  }

  # Base substitutions (shared across all triggers)
  substitutions = {
    _PROJECT_ID = var.project_id
    _REGION     = var.region
  }
}

# Resource for "plan" triggers (runs on PRs)
resource "google_cloudbuild_trigger" "tf_plan" {
  for_each = local.applications # Iterate over applications

  project         = var.project_id
  name            = "${var.repository_name}-${each.key}-${local.plan_config.name_suffix}"
  location        = var.region
  filename        = "cloudbuild.yaml"
  service_account = google_service_account.service_account["cloud-build-deploy"].id

  included_files = each.value.included_files
  ignored_files  = each.value.ignored_files

  # Trigger on pull requests
  repository_event_config {
    repository = google_cloudbuildv2_repository.github_repo.id
    pull_request {
      branch = local.plan_config.branch_regex
    }
  }

  # Merge base substitutions with application-specific substitutions
  substitutions = merge(
    local.substitutions,
    each.value.substitutions, # Application-specific substitutions
    {
      _APPLY_CHANGES = local.plan_config.apply_changes,
      _CONTEXT       = each.key
    }
  )
}

# Resource for "apply" triggers (runs on pushes to main)
resource "google_cloudbuild_trigger" "tf_apply" {
  for_each = local.applications # Iterate over applications

  project         = var.project_id
  name            = "${var.repository_name}-${each.key}-${local.apply_config.name_suffix}"
  location        = var.region
  filename        = "cloudbuild.yaml"
  service_account = google_service_account.service_account["cloud-build-deploy"].id

  included_files = each.value.included_files
  ignored_files  = each.value.ignored_files

  # Trigger on pushes
  repository_event_config {
    repository = google_cloudbuildv2_repository.github_repo.id
    push {
      branch = local.apply_config.branch_regex
    }
  }

  # Merge base substitutions with application-specific substitutions
  substitutions = merge(
    local.substitutions,
    each.value.substitutions, # Application-specific substitutions
    {
      _APPLY_CHANGES = local.apply_config.apply_changes
      _CONTEXT       = each.key
    }
  )
}
