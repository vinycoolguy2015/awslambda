variable "healthcheck_path" {
  description = "URL Path for healthcheck"
  default     = "/api/v1/version"
  type        = string
}

variable "vpc_id" {
default="vpc-6a"
}


variable "aws_region" {
default="us-east-1"
}
variable "application_subnets" {
default=["subnet-1e","subnet-82","subnet-a8"]
}
