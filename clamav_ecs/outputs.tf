output "clamav_lb_dns" {
  value = aws_lb.test_aws_alb.dns_name
}

output "how_to_use" {
  value = "curl -XPOST ${aws_lb.test_aws_alb.dns_name}/api/v1/scan -F FILES=@variables.tf"
}
