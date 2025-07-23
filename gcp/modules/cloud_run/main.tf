resource "google_cloud_run_v2_service" "main" {
  name     = var.name
  location = var.location

  # Set ingress based on the is_public flag
  ingress = var.is_public ? "INGRESS_TRAFFIC_ALL" : "INGRESS_TRAFFIC_INTERNAL_ONLY"

  template {
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
    }
  }
  deletion_protection = false
}