locals {
  cloud_run_services = {
    "api_service" = {
      name            = "api"
      is_public       = false
      container_port  = 8000
      service_account = google_service_account.service_account["api-service"].email
    }
  }
}

# Caddy is the only legitimate caller — invoke this service as the proxy SA,
# not allUsers. Combined with is_public=false (INGRESS_TRAFFIC_INTERNAL_ONLY)
# this is defence in depth: network layer blocks the *.run.app URL, IAM
# layer blocks anything that does reach the service.
data "google_service_account" "proxy_invoker" {
  account_id = "proxy-invoker-${var.repository_name}"
}

module "cloud_run_services" {
  source          = "../../modules/cloud_run"
  for_each        = local.cloud_run_services
  name            = each.value.name
  location        = var.region
  image_url       = "${var.region}-docker.pkg.dev/${var.project_id}/${var.project_id}-gcr-${var.repository_name}/${each.value.name}:${var.image_tag_suffix}"
  is_public       = each.value.is_public
  service_account = each.value.service_account
  container_port  = each.value.container_port
}

resource "google_cloud_run_v2_service_iam_member" "cloud_run_services_invoker" {
  for_each = local.cloud_run_services

  project  = var.project_id
  location = var.region
  name     = each.value.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${data.google_service_account.proxy_invoker.email}"

  depends_on = [
    module.cloud_run_services
  ]
}
