provider "aws" {
  region = var.aws_region
}

module "vpc" {
  source                   = "./vpc"
  vpc_cidr                 = var.vpc_cidr
  subnet_count             = var.subnet_count
  vpc_public_subnet_cidrs  = var.vpc_public_subnet_cidrs
  vpc_private_subnet_cidrs = var.vpc_private_subnet_cidrs
}

module "rds" {
  source             = "./rds"
  db_storage         = var.db_storage
  dbinstance_class   = var.dbinstance_class
  dbuser             = var.dbuser
  dbpassword         = var.dbpassword
  dbsubnet           = module.vpc.rds_subnetgroup
  rds_security_group = [module.vpc.rds_security_group]
  rds_name           = var.rds_name
}

module "webserver" {
  source          = "./autoscaling"
  vpcid           = module.vpc.vpc_id
  lb_sg           = module.vpc.lb_security_group
  public_subnets  = module.vpc.vpc_public_subnets
  private_subnets = module.vpc.vpc_private_subnets
  highcpu         = var.highcpu
  lowcpu          = var.lowcpu
  ami             = var.ami
  instance_type   = var.instance_type
  instance_sg     = module.vpc.instance_security_group
  public_key_path = var.public_key_path
  userdata        = var.userdata

}
