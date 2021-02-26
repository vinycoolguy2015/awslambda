#Deploy Networking Resources

locals {
  private_sn_count = var.management_subnet["count"] + var.devops_subnet["count"] + var.endpoints_subnet["count"]
}


module "networking" {
  source                  = "./networking"
  vpc_cidr                = var.vpc_cidr
  private_sn_count        = local.private_sn_count
  routes                  = var.routes
  create_nat_routes       = false
  create_gateway_routes   = false
  nacl_rules              = var.nacl_rules
  create_nacl_rules       = true
  management_subnet       = var.management_subnet
  devops_subnet           = var.devops_subnet
  endpoints_subnet        = var.endpoints_subnet
  create_managment_subnet = true
  create_devops_subnet    = true
  create_endpoints_subnet = false
  vpc_name                = "test"
}
