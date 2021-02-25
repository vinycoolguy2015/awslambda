variable "vpc_cidr" {}
variable "private_cidrs" {}
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
