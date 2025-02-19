locals {
  cloud_run_services = {
    "${var.context}" = {
      port = 80
      tag  = "latest"
    }
  }
}


data "google_artifact_registry_docker_image" "portfolio_images" {
  for_each      = local.cloud_run_services
  location      = google_artifact_registry_repository.docker_images_repo.location
  repository_id = google_artifact_registry_repository.docker_images_repo.repository_id
  image_name    = "${each.key}:${each.value.tag}"
}

resource "google_cloud_run_v2_service" "portfolio_apps" {
  for_each = local.cloud_run_services

  location = google_artifact_registry_repository.docker_images_repo.location
  name     = each.key
  project  = var.project_id

  template {
    containers {
      image = data.google_artifact_registry_docker_image.portfolio_images[each.key].self_link
      ports {
        container_port = each.value.port
      }
    }
  }
}

resource "google_cloud_run_service_iam_binding" "allusers_run_invoker" {
  service  = google_cloud_run_v2_service.portfolio_apps["${var.context}"].name
  location = google_cloud_run_v2_service.portfolio_apps["${var.context}"].location
  project  = google_cloud_run_v2_service.portfolio_apps["${var.context}"].project

  role = "roles/run.invoker"
  members = [
    "allUsers"
  ]
}
