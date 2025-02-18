locals {
  sa_deploy_roles = [
    "roles/logging.logWriter",
    "roles/iam.serviceAccountUser",
    "roles/monitoring.admin",
    "roles/monitoring.notificationChannelEditor",
    "roles/cloudbuild.builds.builder",
    "roles/serviceusage.serviceUsageViewer",
    "roles/secretmanager.secretAccessor",
    "roles/resourcemanager.projectIamAdmin",
    "roles/artifactregistry.admin",
    "roles/bigquery.admin",
    "roles/cloudfunctions.admin",
    "roles/viewer",
    "roles/storage.admin",
  ]
}

resource "google_project_iam_member" "deploy-bindings" {
  project  = var.project_id
  for_each = toset(local.sa_deploy_roles)
  role     = each.value
  member   = "serviceAccount:${google_service_account.service_account["cloud-build-deploy"].email}"

  depends_on = [google_service_account.service_account]
}