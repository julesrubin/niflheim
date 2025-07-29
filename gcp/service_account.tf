locals {
  service_account = {
    "cloud-build-deploy" = "Cloud Build Deploy Service Account for ${var.repository_name}"
    "proxy-invoker"      = "Service Account for the proxy to invoke other services in the project ${var.repository_name}"
  }
}

resource "google_service_account" "service_account" {
  for_each     = local.service_account
  project      = var.project_id
  account_id   = "${each.key}-${var.repository_name}"
  display_name = each.value
}
