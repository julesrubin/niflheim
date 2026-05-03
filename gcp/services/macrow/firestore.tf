# Firestore Native database for the Macrow service.
#
# Why Firestore: scales to zero, no fixed cost, free tier
# (1 GiB / 50k reads / 20k writes per day) covers this single-user app
# by ~3 orders of magnitude. Document model fits the OFF cache and
# journal data without joins. See claudedocs / discussions for the
# tradeoffs against Cloud SQL, Spanner, etc.

resource "google_project_service" "firestore" {
  project = var.project_id
  service = "firestore.googleapis.com"

  disable_on_destroy = false
}

# Named database (not "(default)") so each service on this project
# can own its own Firestore namespace independently.
#
# Region matches Cloud Run (`europe-west1`) — co-located reads keep
# p50 latency in single-digit ms and avoid cross-region egress.
resource "google_firestore_database" "macrow" {
  project     = var.project_id
  name        = "macrow"
  location_id = var.region
  type        = "FIRESTORE_NATIVE"

  # Default-on; explicit so the choice is auditable. ABANDON means
  # `terraform destroy` removes the resource from state but leaves the
  # database in place. Safer for a personal project; recover via
  # `terraform import` if ever needed.
  deletion_policy = "ABANDON"

  depends_on = [google_project_service.firestore]
}
