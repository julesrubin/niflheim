variable "gcp_subfolders" {
  type    = list(string)
  default = ["gcp/apis", "gcp/portfolio", "gcp"]
}

locals {
  # Base substitutions
  substitutions = {
    _PROJECT_ID = var.project_id
    _REGION     = var.region
  }

  # Define triggers as a map
  triggers = {
    plan = {
      name_suffix   = "tf-plan"
      event_type    = "pull_request"
      branch_regex  = "^main"
      apply_changes = "false"
    }
    apply = {
      name_suffix   = "tf-apply"
      event_type    = "push"
      branch_regex  = "^main"
      apply_changes = "true"
    }
  }
}
resource "google_cloudbuild_trigger" "tf" {
  for_each = { for combo in setproduct(var.gcp_subfolders, keys(local.triggers)) :
    "${replace(combo[0], "/", "-")}-${combo[1]}" => {
      subfolder    = combo[0]
      trigger_type = combo[1]
      config       = local.triggers[combo[1]]
    }
  }

  project         = var.project_id
  name            = "${var.repository_name}-${replace(each.value.subfolder, "/", "-")}-${each.value.config.name_suffix}"
  location        = var.region
  filename        = "cloudbuild.yaml"
  service_account = google_service_account.service_account["cloud-build-deploy"].id

  # Repository event configuration for pull requests
  dynamic "repository_event_config" {
    for_each = each.value.config.event_type == "pull_request" ? [1] : []
    content {
      repository = google_cloudbuildv2_repository.github_repo.id
      pull_request {
        branch = each.value.config.branch_regex
      }
    }
  }

  # Repository event configuration for pushes
  dynamic "repository_event_config" {
    for_each = each.value.config.event_type == "push" ? [1] : []
    content {
      repository = google_cloudbuildv2_repository.github_repo.id
      push {
        branch = each.value.config.branch_regex
      }
    }
  }

  # Merge base substitutions with apply_changes and _SUBFOLDER
  substitutions = merge(local.substitutions, {
    _APPLY_CHANGES = each.value.config.apply_changes
    _SUBFOLDER     = each.value.subfolder
  })

  depends_on = [
    google_service_account.service_account["cloud-build-deploy"],
    google_cloudbuildv2_repository.github_repo,
  ]
}
