# Grant Cloud Build SA access to the Terraform state bucket
resource "google_storage_bucket_iam_member" "tf-state-access" {
  bucket = "${var.project_id}-${var.repository_name}-tfstate"
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.service_account["cloud-build-deploy"].email}"
}

# Grant Cloud Build SA permission to deploy to Cloud Run
resource "google_project_iam_member" "run-deployer-access" {
  project = var.project_id
  role    = "roles/run.admin" # Scoped down from a broad viewer/admin
  member  = "serviceAccount:${google_service_account.service_account["cloud-build-deploy"].email}"
}

resource "google_project_iam_member" "iam-sa-user-access" {
  project = var.project_id
  role    = "roles/iam.serviceAccountUser" # Needed to act as other SAs during deployment
  member  = "serviceAccount:${google_service_account.service_account["cloud-build-deploy"].email}"
}
