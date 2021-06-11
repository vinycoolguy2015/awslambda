
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


module "env" {
  source           = "./compute"
  for_each         = var.environments
  env_name         = each.value
  vpcid            = module.vpc.vpc_id
  public_subnets   = module.vpc.vpc_public_subnets
  private_subnets  = module.vpc.vpc_private_subnets
  highcpu          = var.highcpu
  lowcpu           = var.lowcpu
  ami              = var.ami
  instance_type    = var.instance_type
  public_key_path  = var.public_key_path
  userdata         = var.userdata
  vpc_id           = module.vpc.vpc_id
}

module "codedeploy" {
  source           = "./codedeploy"
  depends_on       = [module.env]
  for_each         = var.environments
  env_name         = each.value
}
