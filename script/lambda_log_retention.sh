#!/bin/bash

# Get all log groups created by AWS Lambda
log_groups=$(aws logs describe-log-groups --log-group-name-prefix /aws/ --query 'logGroups[].logGroupName' --output text)

# Loop through each log group
for log_group in $log_groups; do
  # Update the retention period for the log group to 7 days
  aws logs put-retention-policy --log-group-name "$log_group" --retention-in-days 3

  # Delete all logs older than 7 days
  logs=$(aws logs describe-log-streams --log-group-name "$log_group" --query 'logStreams[?creationTime<=`'$(date -d '3 days ago' +%s)000'`].logStreamName' --output text)

  for log in $logs; do
    response=""
    while [[ "$response" != "" ]]; do
      response=$(aws logs delete-log-stream --log-group-name "$log_group" --log-stream-name "$log" 2>&1)
      if echo "$response" | grep -q "ThrottlingException"; then
        sleep 1
      fi
    done
  done
done
