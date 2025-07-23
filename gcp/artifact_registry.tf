resource "google_artifact_registry_repository" "cloud_run_images" {
  repository_id = "${var.project_id}-gcr-${var.repository_name}"
  format        = "DOCKER"
  location      = var.region
  description   = "Docker repository for Cloud Run service images for ${var.repository_name}"
  project       = var.project_id
}

output "artifact_registry_cloud_run_images_repo_url" {
  description = "The URL of the Docker Artifact Registry repository for Cloud Run images."
  value       = google_artifact_registry_repository.cloud_run_images.name
}
