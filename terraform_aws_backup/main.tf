module "backup" {
  source            = "./backup_module"
  key               = var.key
  value             = var.value
  backup_vault_name = var.backup_vault_name
  rules             = var.rules
  sns_topic_arn     = var.sns_topic_arn
}
