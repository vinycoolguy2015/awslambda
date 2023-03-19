#!/bin/bash
deployment_environment="DEV"
    
project_id=`curl --silent --insecure --header "Content-Type: application/json" --header "Authorization: Bearer MDI3MTUyMjI5NDg5Oq/NJjBrN58" --request GET --url https://bamboo.com/rest/api/latest/deploy/project/forPlan?planKey=TEST |jq '.[0].id'`
    

environment_id=`curl --silent --insecure --header "Content-Type: application/json" --header "Authorization: Bearer MDI3MTUyMjI5NDg5Oq/NJjBrN58" --request GET --url https://bamboo.com/rest/api/latest/deploy/project/$project_id |jq --arg environment $deployment_environment '.environments[] | select(.name == $environment).id'`
    
    
deployment_status=`curl --silent --insecure --header "Content-Type: application/json" --header "Authorization: Bearer MDI3MTUyMjI5NDg5Oq/NJjBrN58" --request GET --url https://bamboo.com/rest/api/latest/deploy/environment/$environment_id/results?max-results=1|jq '.results[0].deploymentState'`
    
echo $deployment_status
