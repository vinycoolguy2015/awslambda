output "security_group_id" {
  value= [for security_group in aws_security_group.security_group: security_group.id]
}
