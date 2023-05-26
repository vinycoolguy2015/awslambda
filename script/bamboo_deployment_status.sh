#!/bin/bash
deployment_environment="SIT"
current_time=`date +%s%3N`
plan_key="TEST"
token="MDQ"

project_id=`curl --silent --insecure --header "Content-Type: application/json" --header "Authorization: Bearer $token"--request GET --url https://bamboo.com/rest/api/latest/deploy/project/forPlan?planKey=$plan_key |jq '.[0].id'`


environment_id=`curl --silent --insecure --header "Content-Type: application/json" --header "Authorization: Bearer $token" --request GET --url https://bamboo.com/rest/api/latest/deploy/project/$project_id |jq --arg environment $deployment_environment '.environments[]| select(.name == $environment).id'`


deployment=`curl --silent --insecure --header "Content-Type: application/json" --header "Authorization: Bearer $token"--request GET --url https://bamboo.com/rest/api/latest/deploy/environment/$environment_id/results?max-results=1|jq '.results[0]'`

deployment_start_date=`echo $deployment|jq '.startedDate'`
deployment_status=`echo $deployment|jq '.deploymentState'|tr -d '"'`

while [ "$deployment_start_date" -gt $current_time ]
do
        echo "Waiting for Deployment to start"
        deployment=`curl --silent --insecure --header "Content-Type: application/json" --header "Authorization: Bearer $token" --request GET --url https://bamboo.com/rest/api/latest/deploy/environment/$environment_id/results?max-results=1|jq '.results[0]'`
        deployment_start_date=`echo $deployment|jq '.startedDate'`
        sleep 10
done
echo "Deployment started"
while [ "$deployment_status" != "SUCCESS" ]
do
  deployment_status=`curl --silent --insecure --header "Content-Type: application/json" --header "Authorization: Bearer $token" --request GET --url https://bamboo.com/rest/api/latest/deploy/environment/$environment_id/results?max-results=1|jq '.results[0].deploymentState'|tr -d '"'`
  echo "Deployment Status: $deployment_status"
  sleep 5
done

echo "Deployment Status: $deployment_status"
