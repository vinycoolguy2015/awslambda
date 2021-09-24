data "aws_db_instance" "database" {
  db_instance_identifier = "database-2"
}

module "backup" {
  source        = "./backup_module"
  key           = var.key
  value         = var.value
  resources_arn = [data.aws_db_instance.database.db_instance_arn]
}
