resource "google_storage_bucket" "bucket" {
  name          = "${var.project_id}-temporary-bucket"
  location      = var.region
  force_destroy = true

  uniform_bucket_level_access = true
}