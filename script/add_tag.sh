#!/bin/bash

for instance in `aws ec2 describe-instances --filters "Name=tag:Name,Values=gms-regression-agent-*" --query 'Reservations[].Instances[].InstanceId'`
  do
    aws ec2 create-tags --resources $instance --tags Key=Name,Value="Test Instance"
  done
