module "security_group" {
  source          = "./sg"
  vpc_id          = var.vpc_id
  security_groups = var.security_groups

}