#Deploy Networking Resources


module "networking" {
  source                = "./networking"
  vpc_cidr              = var.vpc_cidr
  private_sn_count      = var.private_sn_count
  private_cidrs         = [for i in range(1, 255, 2) : cidrsubnet(var.vpc_cidr, 8, i)]
  routes                = var.routes
  create_nat_routes     = false
  create_gateway_routes = false
  nacl_rules            = var.nacl_rules
  create_nacl_rules     = true
}
