key               = "Backup"
value             = "True"
backup_vault_name = "backup_vault"
sns_topic_arn     = "<SNS_TOPIC_ARN>"
rules = [{
  name                     = "daily_snapshot"
  schedule                 = "cron(40 6 ? * MON-SUN *)"
  start_window             = 60
  completion_window        = 180
  delete_after             = 7
  enable_continuous_backup = true
  },
  {
    name                     = "weekly_snapshot"
    schedule                 = "cron(40 16 ? * 1 *)"
    start_window             = 60
    completion_window        = 180
    delete_after             = 30
    enable_continuous_backup = false
  },
  {
    name                     = "monthly_snapshot"
    schedule                 = "cron(0 5 1 * ? *)"
    start_window             = 60
    completion_window        = 180
    delete_after             = 365
    enable_continuous_backup = false
  }
]
