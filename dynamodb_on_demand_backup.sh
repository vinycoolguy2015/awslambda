#!/bin/bash
TABLE='test'
backup_arn=`aws dynamodb create-backup --table-name $TABLE --backup-name test --output text --query BackupDetails.BackupArn`
while true; do
        backup_status=$(aws dynamodb describe-backup  --backup-arn "$backup_arn" --output text --query 'BackupDescription.BackupDetails.BackupStatus')
        echo $backup_status
        if [ "$backup_status" == "AVAILABLE" ]; then
          echo "Table Backup completed successfully."
          break
        else
          echo "Table Backup is in progress"
          sleep 10
        fi
      done
