
locals {
  secret_id = [
  ]
}

resource "google_secret_manager_secret" "secret" {
  for_each  = toset(local.secret_id)
  project   = var.project_id
  secret_id = "${each.value}-${var.repository_name}"
  replication {
    auto {}
  }
}
