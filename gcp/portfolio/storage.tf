resource "google_storage_bucket" "temp" {
  name     = "${var.project_id}-${var.repository_name}-temp"
  location = var.region
}