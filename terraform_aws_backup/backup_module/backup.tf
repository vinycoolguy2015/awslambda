resource "aws_backup_vault" "example-backup-vault" {
  name = var.backup_vault_name
  tags = {
    Role = "backup-vault"
  }
}

resource "aws_backup_plan" "example-backup-plan" {
  name = "${var.backup_vault_name}_plan"
  rule {
    rule_name         = "${var.retention}-day-retention"
    target_vault_name = aws_backup_vault.example-backup-vault.name
    schedule          = var.schedule
    start_window      = var.start_window
    completion_window = var.completion_window
    lifecycle {
      delete_after = var.retention
    }
    recovery_point_tags = {
      Role    = "backup"
      Creator = "aws-backups"
    }
  }
  tags = {
    Role = "backup"
  }
}

resource "aws_backup_selection" "example-server-backup-selection" {
  iam_role_arn = aws_iam_role.example-aws-backup-service-role.arn
  name         = var.name
  plan_id      = aws_backup_plan.example-backup-plan.id
  selection_tag {
    type  = "STRINGEQUALS"
    key   = var.key
    value = var.value
  }
  resources = var.resources_arn
}

