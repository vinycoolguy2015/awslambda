module "subnet" {
  source       = "./subnet"
  subnets      = var.subnets
  vpc_cidr     = var.vpc_cidr
  vpc_name     = var.vpc_name
  vpc_id       = var.vpc_id
  subnet_count = var.subnet_count
}
