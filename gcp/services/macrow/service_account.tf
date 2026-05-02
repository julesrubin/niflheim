locals {
  service_account = {
    "macrow-service" = "Service Account for Macrow service in the project ${var.repository_name}"
  }
}

resource "google_service_account" "service_account" {
  for_each     = local.service_account
  project      = var.project_id
  account_id   = "${each.key}-${var.repository_name}"
  display_name = each.value
}
