resource "google_compute_url_map" "default" {
  name = "main-url-map"

  # Redirect root to /portfolio
  default_url_redirect {
    path_redirect          = "/portfolio"
    redirect_response_code = "MOVED_PERMANENTLY_DEFAULT"
    strip_query            = true
  }

  host_rule {
    hosts        = ["julesrubin.com"]
    path_matcher = "portfolio"
  }

  path_matcher {
    name            = "portfolio"
    default_service = module.portfolio_backend.backend_service_id

    path_rule {
      paths   = ["/portfolio/*"]
      service = module.portfolio_backend.backend_service_id
    }
  }

  # You can add more services here, like /api or /blog, with similar path matchers.
}


resource "google_compute_target_https_proxy" "default" {
  name = "main-https-proxy"

  url_map = google_compute_url_map.default.id
  ssl_certificates = [
    google_compute_managed_ssl_certificate.default.id
  ]
}