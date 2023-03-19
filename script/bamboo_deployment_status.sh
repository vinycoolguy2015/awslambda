#!/bin/bash
deployment_environment="DEV"
current_time=`date +%s`
    
project_id=`curl --silent --insecure --header "Content-Type: application/json" --header "Authorization: Bearer NJjBrN58" --request GET --url https://bamboo.com/rest/api/latest/deploy/project/forPlan?planKey=TEST |jq '.[0].id'`
    

environment_id=`curl --silent --insecure --header "Content-Type: application/json" --header "Authorization: Bearer NJjBrN58" --request GET --url https://bamboo.com/rest/api/latest/deploy/project/$project_id |jq --arg environment $deployment_environment '.environments[] | select(.name == $environment).id'`
    
    
deployment_status=`curl --silent --insecure --header "Content-Type: application/json" --header "Authorization: Bearer NJjBrN58" --request GET --url https://bamboo.com/rest/api/latest/deploy/environment/$environment_id/results?max-results=1|jq '.results[0]'`
    
deployment_start_date=`echo $deployment_status|jq '.startedDate'`
deployment_status=`echo $deployment_status|jq '.deploymentState'`

while [ $deployment_status != "SUCCESS" ]
do
  deployment_status=`curl --silent --insecure --header "Content-Type: application/json" --header "Authorization: Bearer NJjBrN58" --request GET --url https://bamboo.com/rest/api/latest/deploy/environment/$environment_id/results?max-results=1|jq '.results[0].deploymentState'`
  echo $deployment_status
  sleep 5
done
