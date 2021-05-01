output "gateway_url" {
  value = google_api_gateway_gateway.gw.default_hostname
}
