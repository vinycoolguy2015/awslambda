variable "vpc_cidr" {}
variable "vpc_name" {}
variable "private_sn_count" {}
variable "routes" {}
variable "create_gateway_routes" {
  default = false
}
variable "create_nat_routes" {
  default = false
}
variable "create_peering_routes" {
  default = false
}
variable "nacl_rules" {}

variable "create_nacl_rules" {}

variable "management_subnet" {}
variable "devops_subnet" {}
variable "endpoints_subnet" {}

variable "create_managment_subnet" {
  default = false
}
variable "create_devops_subnet" {
  default = false
}
variable "create_endpoints_subnet" {
  default = false
}
