locals {
  applications = {
    root = {
      paths = ["gcp/**"]
      substitutions = {
        _SUBFOLDER = "gcp" # Explicitly define the Terraform root
      }
    },
    # portfolio = {
    #   paths = ["gcp/portfolio/**", "frontend/portfolio/**"]
    #   substitutions = {
    #     _SUBFOLDER = "gcp/portfolio" # Explicitly define the Terraform root
    #   }
    # },
    # apis = {
    #   paths = ["gcp/apis/**"]
    #   substitutions = {
    #     _SUBFOLDER = "gcp/apis" # Explicitly define the Terraform root
    #   }
    # }
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

  # Watch all files in the application's paths (including nested files)
  included_files = [for path in each.value.paths : "${path}/**"]

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
      _APPLY_CHANGES = local.plan_config.apply_changes
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

  included_files = each.value.paths

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
    }
  )
}
