locals {
  cloud_run_services = {
    "macrow_service" = {
      name            = "macrow"
      is_public       = false
      container_port  = 8000
      service_account = google_service_account.service_account["macrow-service"].email
    }
  }
}

# Caddy is the only legitimate caller — invoke this service as the proxy SA,
# not allUsers. Combined with is_public=false (INGRESS_TRAFFIC_INTERNAL_ONLY)
# this is defence in depth: network layer blocks the *.run.app URL, IAM
# layer blocks anything that does reach the service.
data "google_service_account" "proxy_invoker" {
  account_id = "proxy-invoker-${var.repository_name}"
}

module "cloud_run_services" {
  source          = "../../modules/cloud_run"
  for_each        = local.cloud_run_services
  name            = each.value.name
  location        = var.region
  image_url       = "${var.region}-docker.pkg.dev/${var.project_id}/${var.project_id}-gcr-${var.repository_name}/${each.value.name}:${var.image_tag_suffix}"
  is_public       = each.value.is_public
  service_account = each.value.service_account
  container_port  = each.value.container_port

  # Bearer-token guard mounted as $BEARER_TOKEN — the FastAPI dep reads
  # `settings.BEARER_TOKEN` from the env. Secret value is set out-of-band.
  # First-time bootstrap order:
  #   terraform apply -target=google_secret_manager_secret.macrow_secrets
  #   echo -n "<token>" | gcloud secrets versions add niflheim-macrow-bearer-token \
  #       --data-file=- --project portfolio-jrubin
  #   terraform apply   # picks up the version, deploys the Cloud Run revision
  secret_env_vars = {
    BEARER_TOKEN = {
      secret = google_secret_manager_secret.macrow_secrets["bearer-token"].secret_id
    }
  }

  # Cloud Run revisions fail to start if the runtime SA can't read the secret,
  # so the IAM grant must exist before the service mounts the env var.
  depends_on = [
    google_secret_manager_secret_iam_member.macrow_secret_accessors,
  ]
}

resource "google_cloud_run_v2_service_iam_member" "cloud_run_services_invoker" {
  for_each = local.cloud_run_services

  project  = var.project_id
  location = var.region
  name     = each.value.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${data.google_service_account.proxy_invoker.email}"

  depends_on = [
    module.cloud_run_services
  ]
}
