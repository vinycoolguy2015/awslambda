# If you want to setup Backup Auditor, uncomment this file content

#resource "aws_backup_framework" "test" {
#  name        = "Backup_Framework_v1"
#  description = "Backup Audit Manager"
#
#  control {
#    name = "BACKUP_RECOVERY_POINT_MINIMUM_RETENTION_CHECK"

#    input_parameter {
#      name  = "requiredRetentionDays"
#      value = "7"
#    }
#  }

#  control {
#    name = "BACKUP_PLAN_MIN_FREQUENCY_AND_MIN_RETENTION_CHECK"

#    input_parameter {
#      name  = "requiredFrequencyUnit"
#     value = "days"
#    }

#    input_parameter {
#      name  = "requiredRetentionDays"
#      value = "7"
#    }

#    input_parameter {
#      name  = "requiredFrequencyValue"
#      value = "1"
#    }
#  }

#  control {
#    name = "BACKUP_RECOVERY_POINT_ENCRYPTED"
#  }

#  control {
#    name = "BACKUP_RESOURCES_PROTECTED_BY_BACKUP_PLAN"

#    scope {
#      compliance_resource_types = [
#        "EBS", "EC2", "RDS", "DynamoDB"
#      ]
#    }
#  }

#  control {
#    name = "BACKUP_RECOVERY_POINT_MANUAL_DELETION_DISABLED"
#  }
#  control {
#    name = "BACKUP_LAST_RECOVERY_POINT_CREATED"
#    scope {
#      compliance_resource_types = [
#        "EBS", "EC2", "RDS", "DynamoDB"
#      ]
#    }
#  }

#  tags = {
#    "Name" = "Backup Audit Manager"
#  }
#}
