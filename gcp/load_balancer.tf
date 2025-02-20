# # Define the URL map to route requests to the correct backend service
# resource "google_compute_url_map" "default" {
#   name = "main-url-map"

#   # Default service routing to the portfolio backend
#   default_service = module.portfolio_backend.backend_service_self_link
# }

# # Define the target HTTPS proxy, which uses the URL map
# resource "google_compute_target_https_proxy" "default" {
#   name             = "main-https-proxy"
#   url_map          = google_compute_url_map.default.self_link
#   ssl_certificates = [google_compute_managed_ssl_certificate.default.self_link]
# }

# resource "google_compute_global_forwarding_rule" "https" {
#   name                  = "https-forwarding-rule"
#   target                = google_compute_target_https_proxy.default.self_link
#   load_balancing_scheme = "EXTERNAL_MANAGED"
#   port_range            = "80"
#   ip_protocol           = "TCP"
#   ip_address            = google_compute_global_address.default_static_ip.address
# }

resource "google_compute_url_map" "default" {
  name = "main-url-map"

  default_service = module.portfolio_backend.backend_service_id
}

resource "google_compute_target_https_proxy" "default" {
  name = "main-https-proxy"

  url_map = google_compute_url_map.default.id
  ssl_certificates = [
    google_compute_managed_ssl_certificate.default.id
  ]
}