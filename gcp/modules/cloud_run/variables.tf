variable "name" {
  type        = string
  description = "The name of the Cloud Run service."
}

variable "location" {
  type        = string
  description = "The GCP region where the service will be deployed."
}

variable "image_url" {
  type        = string
  description = "The URL of the container image to deploy."
}

variable "is_public" {
  type        = bool
  description = "If true, the service will be publicly accessible. If false, it will be internal only."
  default     = false # Default to private for security
}

variable "env_vars" {
  type        = map(string)
  description = "A map of environment variables to set in the container."
  default     = {}
}

variable "container_port" {
  type        = number
  description = "The port the container listens on."
  default     = 8080
}
