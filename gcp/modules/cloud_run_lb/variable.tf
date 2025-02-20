variable "name" {
  description = "Name of the Cloud Run service backend."
  type        = string
}

variable "cloud_run_service" {
  description = "The name of the Cloud Run service to attach."
  type        = string
}

variable "region" {
  description = "Region where the service is deployed."
  type        = string
}
