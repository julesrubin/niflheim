variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "project_number" {
  description = "The GCP project number"
  type        = string
}

variable "region" {
  description = "The GCP region"
  type        = string
  default     = "europe-west1"
}

variable "repository_name" {
  description = "The name of the repository"
  type        = string

}

variable "owner" {
  description = "The repository owner"
  type        = string
}

variable "github_token_secret" {
  description = "The secret ID for the GitHub token"
  type        = string
}
