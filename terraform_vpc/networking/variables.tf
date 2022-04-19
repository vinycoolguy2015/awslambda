variable "vpc_cidr" {}
variable "vpc_name" {}
variable "subnet_count" {}
variable "private_subnet" {}
variable "public_subnet" {}
variable "nacl_rules"  { default={"private" = {},"public" = {}}}
