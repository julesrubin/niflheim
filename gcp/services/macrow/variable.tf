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