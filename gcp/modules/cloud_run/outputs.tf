output "url" {
  description = "The URL of the deployed Cloud Run service."
  value       = google_cloud_run_v2_service.main.uri
}

output "service_id" {
  description = "The full ID of the Cloud Run service."
  value       = google_cloud_run_v2_service.main.id
}

output "service_account" {
  description = "The service account used by the service revision."
  value       = google_cloud_run_v2_service.main.template[0].service_account
}

output "name" {
  description = "The name of the service."
  value       = google_cloud_run_v2_service.main.name
}

output "location" {
  description = "The location of the service."
  value       = google_cloud_run_v2_service.main.location
}

output "project" {
  description = "The project ID of the service."
  value       = google_cloud_run_v2_service.main.project
}