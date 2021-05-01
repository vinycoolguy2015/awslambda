#!/bin/bash
project=terraform-312414
cloudrun_url=$(gcloud run services describe app --platform managed --project $project --region us-east1 --format 'value(status.url)' | cut -d '/' -f3)
sed -i "s/CLOUD_RUN_URL/$cloudrun_url/g" ~/gcp_cloudrun_apigateway/api_gateway/spec.yaml
