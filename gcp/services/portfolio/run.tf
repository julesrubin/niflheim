locals {
  cloud_run_services = {
    "portfolio_service" = {
      name      = "portfolio"
      is_public = true
    }
  }
}

module "cloud_run_services" {
  source    = "../../modules/cloud_run"
  for_each  = local.cloud_run_services
  name      = each.value.name
  location  = var.region
  image_url = "${var.region}-docker.pkg.dev/${var.project_id}/${var.project_id}-gcr-${var.repository_name}/${each.value.name}:${var.image_tag_suffix}"
  is_public = each.value.is_public
}

resource "google_cloud_run_v2_service_iam_member" "cloud_run_services_invoker" {
  for_each = local.cloud_run_services

  project  = var.project_id
  location = var.region
  name     = each.value.name
  role     = "roles/run.invoker"
  member   = "allUsers"

  depends_on = [
    module.cloud_run_services
  ]
}
