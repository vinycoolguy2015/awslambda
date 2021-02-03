#!/bin/bash

for dir in $(find environments/qa -type d -maxdepth 2 -mindepth 2); do
  printf  '\nChecking Directory: %s \n' "$dir"
  cd -
  cd $dir
  terragrunt init -plugin-dir=../../terraform_aws_plugins/plugins/darwin_amd64 
  terragrunt plan --detailed-exitcode -out=tf.plan 2> /dev/null || ec=$?
  case $ec in
  0) echo "No Changes Found": exit 0;;
  1) printf '%s/n' "Command exited with non-zero.Check issues with terragrunt code";;
  2) echo "Changes found";
     MESSAGE=$(terraform show -no-color tf.plan| awk '/#/,EOF { print $0 }');
     #curl -X POST -H 'Content-type: application/json' --data "{'text':'$MESSAGE'}" <Slack_Webhook_URL>
     echo $MESSAGE
  esac
done






