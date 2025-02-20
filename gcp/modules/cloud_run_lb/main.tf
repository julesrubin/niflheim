resource "google_compute_region_network_endpoint_group" "neg" {
  name                  = var.name
  network_endpoint_type = "SERVERLESS"
  region                = var.region

  cloud_run {
    service = var.cloud_run_service
  }
}

resource "google_compute_backend_service" "backend" {
  name                  = "${var.name}-backend"
  load_balancing_scheme = "EXTERNAL_MANAGED"
  protocol              = "HTTP"
  timeout_sec           = 30

  backend {
    group = google_compute_region_network_endpoint_group.neg.id
  }
}
