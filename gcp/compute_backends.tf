# module "default_backend" {
#   source            = "./modules/cloud_run_lb"
#   name              = "default"
#   cloud_run_service = "default-service"
#   region            = "europe-west1"
# }

module "portfolio_backend" {
  source            = "./modules/cloud_run_lb"
  name              = "portfolio"
  cloud_run_service = "portfolio"
  region            = "europe-west1"
}
