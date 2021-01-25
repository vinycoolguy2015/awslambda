#!/bin/bash
terraform plan --detailed-exitcode -out=tf.plan 2> /dev/null || ec=$?
case $ec in 
0) echo "No Changes Found": exit 0;;
1) printf '%s/n' "Command exited with non-zero";exit 1;;
2) echo "Changes found";
   MESSAGE=$(terraform show -no-color tf.plan| awk '/#/,EOF { print $0 }');
   curl -X POST -H 'Content-type: application/json' --data "{'text':'$MESSAGE'}" <Slack_Webhook_URL>
esac
