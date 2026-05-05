resource "google_cloud_run_v2_service" "main" {
  name     = var.name
  location = var.location

  # Set ingress based on the is_public flag
  ingress = var.is_public ? "INGRESS_TRAFFIC_ALL" : "INGRESS_TRAFFIC_INTERNAL_ONLY"

  template {
    service_account = var.service_account
    containers {
      image = var.image_url
      ports {
        container_port = var.container_port
      }

      # Dynamically add environment variables if any are provided
      dynamic "env" {
        for_each = var.env_vars
        content {
          name  = env.key
          value = env.value
        }
      }

      # Secret-backed env vars — sourced from Secret Manager at instance start.
      # Map shape: { ENV_NAME = { secret = "<secret_id>", version = "latest" } }.
      dynamic "env" {
        for_each = var.secret_env_vars
        content {
          name = env.key
          value_source {
            secret_key_ref {
              secret  = env.value.secret
              version = env.value.version
            }
          }
        }
      }
    }
  }
  deletion_protection = false
}