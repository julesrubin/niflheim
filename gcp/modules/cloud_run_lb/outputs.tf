output "backend_service_id" {
  description = "The ID of the backend service created for the Cloud Run service."
  value       = google_compute_backend_service.backend.id
}

output "network_endpoint_group" {
  description = "The ID of the network endpoint group associated with the Cloud Run service."
  value       = google_compute_region_network_endpoint_group.neg.id
}
