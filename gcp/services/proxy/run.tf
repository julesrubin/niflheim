
locals {
  proxied_cloud_run_services = [
    "portfolio",
    "api",
  ]
}

data "google_service_account" "proxy_invoker" {
  account_id = "proxy-invoker-${var.repository_name}"
}

module "proxy_service" {
  source          = "../../modules/cloud_run"
  name            = "proxy-service"
  location        = var.region
  image_url       = "${var.region}-docker.pkg.dev/${var.project_id}/${var.project_id}-gcr-${var.repository_name}/proxy:${var.image_tag_suffix}"
  is_public       = true
  service_account = data.google_service_account.proxy_invoker.email
  env_vars = {
    for v in local.proxied_cloud_run_services :
    "${upper(v)}_SERVICE_URL" => "https://${v}-${var.project_number}.${var.region}.run.app"
  }
}

resource "google_cloud_run_v2_service_iam_member" "allow_all_users_to_invoke_proxy" {
  project  = module.proxy_service.project
  location = module.proxy_service.location
  name     = module.proxy_service.name
  role     = "roles/run.invoker"
  member   = "allUsers"

  depends_on = [
    module.proxy_service
  ]
}
