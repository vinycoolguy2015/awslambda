output "vpc_endpoint" {
  value       = aws_transfer_server.osg.endpoint_details[0].vpc_endpoint_id
  description = "VPC Endpoint of transfer server"
}

output "id" {
  value       = aws_transfer_server.osg.id
  description = "ID of transfer server"
}

output "endpoint" {
  value       = aws_transfer_server.osg.endpoint
  description = "Endpoint of transfer server"
}

output "endpoint-dns" {
  value = data.local_file.endpoint-dns.content
}
