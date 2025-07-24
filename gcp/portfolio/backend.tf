terraform {
  required_version = ">= 0.15" # Specify the minimum Terraform version
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.18.0" # Make sure the version fits your needs
    }
  }

  backend "gcs" {
    bucket = "${var.project_id}-${var.repository_name}-tfstate"
    prefix = var.context
  }
}
