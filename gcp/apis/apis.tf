# echo "GCP basic APIs activation: "
# echo "serviceusage.googleapis.com, "
# echo "cloudresourcemanager.googleapis.com, "
# echo "cloudbuild.googleapis.com, "
# echo "artifactregistry.googleapis.com"
# echo "******"

locals {
  apis = [
    "serviceusage.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "cloudbuild.googleapis.com",
    "artifactregistry.googleapis.com"
  ]
}

# activate basic APIs
resource "google_project_service" "serviceusage" {
  for_each = toset(local.apis)

  project = var.project_id
  service = each.key
}
