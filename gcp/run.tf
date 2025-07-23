module "hello_service" {
  source    = "./modules/cloud_run"
  name      = "hello"
  location  = var.region
  image_url = "us-docker.pkg.dev/cloudrun/container/hello"
  is_public = true
}

module "hello_2_service" {
  source    = "./modules/cloud_run"
  name      = "hello-2"
  location  = var.region
  image_url = "us-docker.pkg.dev/cloudrun/container/hello"
  is_public = true
}

module "proxy_service" {
  source    = "./modules/cloud_run"
  name      = "proxy-service"
  location  = var.region
  image_url = "europe-west1-docker.pkg.dev/sandbox-jrubin/sandbox-jrubin-gcr-niflheim/proxy"
  is_public = true
  env_vars = {
    HELLO_SERVICE_URL   = "${module.hello_service.url}"
    HELLO_2_SERVICE_URL = "${module.hello_2_service.url}"
  }
}

resource "google_cloud_run_v2_service_iam_member" "allow_proxy_to_hello" {
  project  = module.hello_service.project
  location = module.hello_service.location
  name     = module.hello_service.name
  role     = "roles/run.invoker"
  member   = "allUsers" # TODO : find a way to use the proxy service account here
}

resource "google_cloud_run_v2_service_iam_member" "allow_proxy_to_hello_2" {
  project  = module.hello_2_service.project
  location = module.hello_2_service.location
  name     = module.hello_2_service.name
  role     = "roles/run.invoker"
  member   = "allUsers" # TODO : find a way to use the proxy service account here
}

resource "google_cloud_run_v2_service_iam_member" "allow_all_users_to_invoke_proxy" {
  project  = module.proxy_service.project
  location = module.proxy_service.location
  name     = module.proxy_service.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
