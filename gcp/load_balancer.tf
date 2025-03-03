resource "google_compute_url_map" "default" {
  name = "main-url-map"

  # Serve the portfolio as the default service (handles "/")
  default_service = module.portfolio_backend.backend_service_id

  host_rule {
    hosts        = ["julesrubin.com"]
    path_matcher = "portfolio"
  }

  path_matcher {
    name            = "portfolio"
    default_service = module.portfolio_backend.backend_service_id
  }
}

resource "google_compute_target_https_proxy" "default" {
  name = "main-https-proxy"

  url_map = google_compute_url_map.default.id
  ssl_certificates = [
    google_compute_managed_ssl_certificate.default.id
  ]
}
