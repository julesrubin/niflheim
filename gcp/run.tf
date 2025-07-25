locals {
  cloud_run_services = {
    "hello_service" = {
      name      = "hello"
      image_url = "us-docker.pkg.dev/cloudrun/container/hello"
      is_public = true
    }
    "portfolio_service" = {
      name      = "portfolio"
      image_url = "europe-west1-docker.pkg.dev/sandbox-jrubin/sandbox-jrubin-gcr-niflheim/portfolio"
      is_public = true
    }
  }
}

module "cloud_run_services" {
  source    = "./modules/cloud_run"
  for_each  = local.cloud_run_services
  name      = each.value.name
  location  = var.region
  image_url = each.value.image_url
  is_public = each.value.is_public
}

resource "google_cloud_run_v2_service_iam_member" "cloud_run_services_invoker" {
  for_each = local.cloud_run_services

  project  = var.project_id
  location = var.region
  name     = each.value.name
  role     = "roles/run.invoker"
  member   = "allUsers" # TODO : find a way to use the service account here

  depends_on = [
    module.cloud_run_services
  ]
}

module "proxy_service" {
  source    = "./modules/cloud_run"
  name      = "proxy-service"
  location  = var.region
  image_url = "europe-west1-docker.pkg.dev/sandbox-jrubin/sandbox-jrubin-gcr-niflheim/proxy"
  is_public = true
  env_vars = {
    for k, v in local.cloud_run_services :
    "${upper(k)}_URL" => module.cloud_run_services[k].url
  }

  depends_on = [module.cloud_run_services]
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
