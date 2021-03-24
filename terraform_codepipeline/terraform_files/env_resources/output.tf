output "Application_Address" {
  value = "http://${aws_lb.web.dns_name}"
}

