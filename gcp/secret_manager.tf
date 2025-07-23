resource "google_secret_manager_secret" "github_token" {
  project   = var.project_id
  secret_id = "github-token"

  replication {
    auto {}
  }
}
# TODO: Update README to explain how to set the secret value