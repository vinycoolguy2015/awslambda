#!/bin/bash

echo "Stopping Canary"
aws synthetics stop-canary --name lamp --region us-west-2
canary_state=`aws synthetics get-canary --name lamp --region us-west-2 | jq '.Canary.Status.State'|tr -d '"'`

while [ "$canary_state" != "STOPPED" ]; do
 echo $canary_state
 canary_state=`aws synthetics get-canary --name lamp --region us-west-2 | jq '.Canary.Status.State'|tr -d '"'`
        sleep 5
done

echo "Canary Stopped.Changing index.php file"
sudo sed -i 's/Welcome to the AWS CloudFormation PHP Sample./Welcome to the AWS CloudFormation PHP Sample.My name is Vinayak Pandey/g' /var/www/html/index.php
sudo service httpd restart

echo "Starting Canary"
aws synthetics update-canary --name lamp --visual-reference '{"BaseCanaryRunId": "nextRun"}' --region us-west-2
aws synthetics start-canary --name lamp --region us-west-2
