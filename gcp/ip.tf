resource "google_compute_global_address" "default_static_ip" {
  name = "default-static-ip"
}


# Define the SSL certificate for julesrubin.com
resource "google_compute_managed_ssl_certificate" "default" {
  name = "default-ssl-cert"
  managed {
    domains = ["julesrubin.com"]
  }
}

resource "google_compute_global_forwarding_rule" "default" {
  name = "default-forwarding-rule"

  target     = google_compute_target_https_proxy.default.id
  port_range = "443"
  ip_address = google_compute_global_address.default_static_ip.address
}