locals {
  cloud_build_sa_email = "serviceAccount:${google_service_account.service_account["cloud-build-deploy"].email}"

  cloud_build_project_roles = {
    "run-deployer-access" = {
      role        = "roles/run.admin"
      description = "Grant Cloud Build SA permission to deploy to Cloud Run"
    }
    "iam-sa-user-access" = {
      role        = "roles/iam.serviceAccountUser"
      description = "Needed to act as other SAs during deployment"
    }
    "logging-writer-access" = {
      role        = "roles/logging.logWriter"
      description = "Grant Cloud Build SA the right to write logs"
    }
    "secret-manager-access" = {
      role        = "roles/secretmanager.secretAccessor"
      description = "Grant Cloud Build SA access to Secret Manager"
    }
    "storage-admin-access" = {
      role        = "roles/storage.admin"
      description = "Grant Cloud Build SA storage admin role (for GCS bucket IAM policy access)"
    }
    "secretmanager-admin-access" = {
      role        = "roles/secretmanager.admin"
      description = "Grant Cloud Build SA Secret Manager admin role"
    }
    "cloudbuild-build-access" = {
      role        = "roles/cloudbuild.builds.builder"
      description = "Grant Cloud Build SA permission to run builds"
    }
    "cloudbuild-connection-access" = {
      role        = "roles/cloudbuild.connectionAdmin"
      description = "Grant Cloud Build SA permission to view connections"
    }
    "project-iam-admin-access" = {
      role        = "roles/resourcemanager.projectIamAdmin"
      description = "Grant Cloud Build SA Project IAM Admin role (to manage project-level IAM policies)"
    }
    "service-account-admin-access" = {
      role        = "roles/iam.serviceAccountAdmin"
      description = "Grant Cloud Build SA Service Account Admin role (to manage service accounts)"
    }
  }
}

# Grant Cloud Build SA access to the Terraform state bucket
resource "google_storage_bucket_iam_member" "tf-state-access" {
  bucket = "${var.project_id}-${var.repository_name}-tfstate"
  role   = "roles/storage.objectAdmin"
  member = local.cloud_build_sa_email
}

# Grant various project-level roles to the Cloud Build SA
resource "google_project_iam_member" "cloud_build_project_roles" {
  for_each = local.cloud_build_project_roles

  project = var.project_id
  role    = each.value.role
  member  = local.cloud_build_sa_email
}
