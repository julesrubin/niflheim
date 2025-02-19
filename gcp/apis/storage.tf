resource "google_storage_bucket" "temporary_bucket" {
  name          = "${var.project_id}-temporary-bucket-${var.context}"
  project       = var.project_id
  location      = var.region
  force_destroy = true
}