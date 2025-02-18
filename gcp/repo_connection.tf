resource "google_cloudbuildv2_repository" "github_repo" {
  project           = var.project_id
  location          = var.region
  name              = var.repository_name
  parent_connection = "projects/${var.project_id}/locations/${var.region}/connections/github_connection"
  remote_uri        = "https://github.com/${var.owner}/${var.repository_name}.git"
}
