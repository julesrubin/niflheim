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
  for_each = local.triggers

  project         = var.project_id
  name            = "${var.repository_name}-${each.value.name_suffix}"
  location        = var.region
  filename        = "cloudbuild.yaml"
  service_account = google_service_account.service_account["cloud-build-deploy"].id

  # Dynamic repository event configuration for pull requests
  dynamic "repository_event_config" {
    for_each = each.value.event_type == "pull_request" ? [1] : []
    content {
      repository = google_cloudbuildv2_repository.github_repo.id
      pull_request {
        branch = each.value.branch_regex
      }
    }
  }

  # Dynamic repository event configuration for pushes
  dynamic "repository_event_config" {
    for_each = each.value.event_type == "push" ? [1] : []
    content {
      repository = google_cloudbuildv2_repository.github_repo.id
      push {
        branch = each.value.branch_regex
      }
    }
  }

  # Merge base substitutions with apply_changes
  substitutions = merge(local.substitutions, {
    _APPLY_CHANGES = each.value.apply_changes
  })

  depends_on = [
    google_service_account.service_account["cloud-build-deploy"],
    google_cloudbuildv2_repository.github_repo,
  ]
}
