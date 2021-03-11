module "security_group" {
  source               = "./sg"
  vpc_id               = var.vpc_id
  security_group_name  = var.security_group_name
  security_group_rules = var.security_group_rules
  description          = var.description
}
