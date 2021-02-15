#!/bin/bash
aws rds describe-db-instances --query 'DBInstances[*].{DB:DBInstanceIdentifier,Auto:AutoMinorVersionUpgrade,Window:PreferredMaintenanceWindow}' --region ap-southeast-1 --output table
