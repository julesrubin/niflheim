locals {
  secrets = {
    "default-client-credentials" = {
      labels = {
        service = "${var.repository_name}-${var.context}"
        type    = "client-credentials"
      }
    }
    "${var.repository_name}-${var.context}-jwt-signing-key" = {
      labels = {
        service = "${var.repository_name}-${var.context}"
        type    = "jwt-signing-key"
      }
    }
  }
}

resource "google_secret_manager_secret" "api_secrets" {
  for_each  = local.secrets
  project   = var.project_id
  secret_id = "${var.repository_name}-${var.context}-${each.key}"

  labels = each.value.labels

  replication {
    auto {}
  }
}
