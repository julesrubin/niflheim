variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The GCP region"
  type        = string
}

# Firestore locations are a separate namespace from Cloud Run regions even
# though both spell europe-west1 the same way. Default keeps them aligned;
# split if a future region change needs to leave Firestore where it is.
variable "firestore_location" {
  description = "Firestore Native database location (defaults to region)."
  type        = string
  default     = ""
}

variable "repository_name" {
  description = "The name of the repository"
  type        = string
}

variable "context" {
  description = "The context of the project"
  type        = string
}

variable "image_tag_suffix" {
  description = "Suffix for the Docker image tag (e.g., commit SHA)"
  type        = string
  default     = "latest"
}