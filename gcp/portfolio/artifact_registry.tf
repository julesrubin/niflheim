resource "google_artifact_registry_repository" "docker_images_repo" {
  project       = var.project_id
  repository_id = "${var.project_id}-gcr-${var.repository_name}-${var.context}"
  location      = var.region
  description   = "Repository for storing Docker images for the ${title(var.repository_name)}, ${var.context} project"
  format        = "DOCKER"

  docker_config {
    immutable_tags = false # Ensures images cannot be overwritten
  }
}
