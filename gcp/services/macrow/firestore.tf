# Firestore Native database for the Macrow service.
#
# Why Firestore: scales to zero, no fixed cost, free tier
# (1 GiB / 50k reads / 20k writes per day) covers this single-user app
# by ~3 orders of magnitude. Document model fits the OFF cache and
# journal data without joins. See claudedocs / discussions for the
# tradeoffs against Cloud SQL, Spanner, etc.
#
# Note: firestore.googleapis.com is enabled out-of-band (`gcloud services
# enable`), matching the rest of this repo's API-management pattern. The
# Cloud Build SA does not hold roles/serviceusage.serviceUsageAdmin, so a
# `google_project_service` resource here would fail at apply.

# Named database (not "(default)") so each service on this project
# can own its own Firestore namespace independently.
#
# Region matches Cloud Run (`europe-west1`) — co-located reads keep
# p50 latency in single-digit ms and avoid cross-region egress.
resource "google_firestore_database" "macrow" {
  project     = var.project_id
  name        = "macrow"
  location_id = var.firestore_location != "" ? var.firestore_location : var.region
  type        = "FIRESTORE_NATIVE"

  # Default-on; explicit so the choice is auditable. ABANDON means
  # `terraform destroy` removes the resource from state but leaves the
  # database in place. Safer for a personal project; recover via
  # `terraform import` if ever needed.
  deletion_policy = "ABANDON"
}
