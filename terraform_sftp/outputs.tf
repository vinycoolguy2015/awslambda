output "vpc_endpoint" {
  value       = aws_transfer_server.sftp.endpoint_details[0].vpc_endpoint_id
  description = "VPC Endpoint of transfer server"
}

output "id" {
  value       = aws_transfer_server.sftp.id
  description = "ID of transfer server"
}

output "endpoint" {
  value       = aws_transfer_server.sftp.endpoint
  description = "Endpoint of transfer server"
}

output "endpoint-dns" {
  value = data.local_file.endpoint-dns.content
}
