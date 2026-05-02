resource "google_secret_manager_secret_iam_member" "macrow_service_access" {
  for_each  = google_secret_manager_secret.macrow_secrets
  project   = var.project_id
  secret_id = each.value.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.service_account["macrow-service"].email}"
  depends_on = [
    google_secret_manager_secret.macrow_secrets,
    google_service_account.service_account["macrow-service"]
  ]
}
