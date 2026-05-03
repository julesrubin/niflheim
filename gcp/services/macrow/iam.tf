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

# Grant the macrow Cloud Run service account read/write access on
# the project's Firestore data. `roles/datastore.user` covers
# Firestore Native (despite the legacy "datastore" naming).
#
# Project-scoped because Firestore IAM doesn't yet support per-database
# bindings via a dedicated resource. This project hosts only macrow's
# Firestore data, so the blast radius is naturally limited; if another
# service ever needs Firestore here, switch to IAM conditions on
# `resource.name`.
resource "google_project_iam_member" "macrow_datastore_user" {
  project = var.project_id
  role    = "roles/datastore.user"
  member  = "serviceAccount:${google_service_account.service_account["macrow-service"].email}"

  depends_on = [google_firestore_database.macrow]
}
