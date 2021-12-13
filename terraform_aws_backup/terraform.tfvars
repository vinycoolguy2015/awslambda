key               = "Name"
value             = "database"
backup_vault_name = "test"
sns_topic_arn     = "arn:aws:sns:us-east-1:xyz:patching"
rules = [{
  name                     = "daily_snapshot"
  schedule                 = "cron(40 6 ? * MON-SAT *)"
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
