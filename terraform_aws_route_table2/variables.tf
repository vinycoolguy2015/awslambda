variable "aws_region" {
  default = "us-west-2"
}

variable "vpc_cidr" {}

variable "routes" {}


variable "nacl_rules" {}
variable "management_subnet" {}
variable "devops_subnet" {}
variable "endpoints_subnet" {}
