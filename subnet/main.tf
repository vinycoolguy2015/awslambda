#Deploy Networking Resources

module "subnet" {
  source       = "./subnet"
  for_each     = var.subnets
  subnet_count = each.value.count
  vpc_cidr     = var.vpc_cidr
  vpc_name     = var.vpc_name
  vpc_id       = var.vpc_id
  subnet_name  = each.key
  newbits      = each.value.newbits
  netnum       = each.value.netnum
  routes       = each.value.routes
  nacl_rules   = each.value.nacl_rules
}
