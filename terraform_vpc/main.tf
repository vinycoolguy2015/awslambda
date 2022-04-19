
locals {
  subnet_count = var.private_subnet["count"] + var.public_subnet["count"] 
}


module "networking" {
  source                  = "./networking"
  vpc_cidr                = var.vpc_cidr
  subnet_count            = local.subnet_count
  private_subnet          = var.private_subnet
  public_subnet           = var.public_subnet
  vpc_name                = "test"
}
