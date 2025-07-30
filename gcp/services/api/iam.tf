resource "google_secret_manager_secret_iam_member" "api_service_access" {
  for_each  = google_secret_manager_secret.api_secrets
  project   = var.project_id
  secret_id = each.key
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.service_account["api-service"].email}"
  depends_on = [
    google_secret_manager_secret.api_secrets,
    google_service_account.service_account["api-service"]
  ]
}