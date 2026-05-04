# Grant the macrow Cloud Run service account read/write access on
# Firestore. `roles/datastore.user` covers Firestore Native (despite the
# legacy "datastore" naming).
#
# Scoped via IAM condition to the `macrow` database only — the SA gets no
# access to any other Firestore database that lives or might land on this
# project, so a future second service can't accidentally inherit access.
resource "google_project_iam_member" "macrow_datastore_user" {
  project = var.project_id
  role    = "roles/datastore.user"
  member  = "serviceAccount:${google_service_account.service_account["macrow-service"].email}"

  condition {
    title       = "macrow-db-only"
    description = "Restrict roles/datastore.user to the macrow Firestore database."
    expression  = "resource.name == \"projects/${var.project_id}/databases/macrow\""
  }

  depends_on = [google_firestore_database.macrow]
}
