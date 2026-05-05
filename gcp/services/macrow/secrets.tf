# Secret Manager secrets owned by the macrow service.
#
# Single bearer-token entry today; the locals-map shape mirrors
# `gcp/services/api/secrets.tf` so adding the next secret (Firebase service
# account, JWT signing key, etc.) is a one-line map entry — IAM accessor
# bindings in iam.tf already iterate `for_each` over this resource.
#
# Secret values are set out-of-band:
#   echo -n "<token>" | gcloud secrets versions add niflheim-macrow-bearer-token \
#       --data-file=- --project portfolio-jrubin
#
# `gcloud secrets versions add` is intentionally not Terraformed: secret
# values must never live in plan output, state, or backend buckets.

locals {
  secrets = {
    "bearer-token" = {
      labels = {
        service = var.repository_name
        context = var.context
        type    = "bearer-token"
      }
    }
  }
}

resource "google_secret_manager_secret" "macrow_secrets" {
  for_each = local.secrets

  project   = var.project_id
  secret_id = "${var.repository_name}-${var.context}-${each.key}"

  labels = each.value.labels

  replication {
    auto {}
  }
}
