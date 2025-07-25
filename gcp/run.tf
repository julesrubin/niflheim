# locals {
#   cloud_run_services = {
#     "portfolio_service" = {
#       name      = "portfolio"
#       is_public = true
#     }
#   }
# }

# module "cloud_run_services" {
#   source    = "./modules/cloud_run"
#   for_each  = local.cloud_run_services
#   name      = each.value.name
#   location  = var.region
#   image_url = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.cloud_run_images.name}/${each.value.name}:${var.image_tag_suffix}"
#   is_public = each.value.is_public
# }

# resource "google_cloud_run_v2_service_iam_member" "cloud_run_services_invoker" {
#   for_each = local.cloud_run_services

#   project  = var.project_id
#   location = var.region
#   name     = each.value.name
#   role     = "roles/run.invoker"
#   member   = "allUsers" # TODO : find a way to use the service account here

#   depends_on = [
#     module.cloud_run_services
#   ]
# }

# module "proxy_service" {
#   source    = "./modules/cloud_run"
#   name      = "proxy-service"
#   location  = var.region
#   image_url = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.cloud_run_images.name}/proxy:${var.image_tag_suffix}"
#   is_public = true
#   env_vars = {
#     for k, v in local.cloud_run_services :
#     "${upper(k)}_URL" => module.cloud_run_services[k].url
#   }

#   depends_on = [module.cloud_run_services]
# }

# resource "google_cloud_run_v2_service_iam_member" "allow_all_users_to_invoke_proxy" {
#   project  = module.proxy_service.project
#   location = module.proxy_service.location
#   name     = module.proxy_service.name
#   role     = "roles/run.invoker"
#   member   = "allUsers"

#   depends_on = [
#     module.proxy_service
#   ]
# }
