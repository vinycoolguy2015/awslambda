import json
import boto3

sns_client = boto3.client('sns',region_name='ap-southeast-1')

exempted_cves=['CWE-319','CWE-117','CWE-93']
exempted_functions=['lambdaA','basicauth']

def lambda_inspector_findings(region):
    inspector = boto3.client('inspector2',region_name=region)
    paginator = inspector.get_paginator('list_findings')
    page_iterator = paginator.paginate(filterCriteria={
                'findingStatus': [
                    {
                        'comparison': 'EQUALS',
                        'value': 'ACTIVE'
                    },
                ],
                'resourceType': [
                    {
                        'comparison': 'EQUALS',
                        'value': 'AWS_LAMBDA_FUNCTION'
                    },
                ],
            })

    for data in page_iterator:
        for finding in data['findings']:
            suppress_finding=False
            for exempted_cve in exempted_cves:
                if exempted_cve in finding['title']:
                    suppress_finding=True
                    break
            if suppress_finding==False:
                for resource in finding['resources']:
                    if resource['details']['awsLambdaFunction']['functionName'] not in exempted_functions:
                        message = {"version": "1.0","source": "custom","content": {
        "description": finding['title'] +" vulnerability found in Lambda function: "+resource['id']}}
                        sns_client.publish(TargetArn='arn:aws:sns:ap-southeast-1:091308437569:ecr_scan_findings',
                                Message=json.dumps({'default': json.dumps(message)}),
                                MessageStructure='json')
                                
    

def lambda_handler(event, context):
    lambda_inspector_findings("us-east-1")
    lambda_inspector_findings("ap-southeast-1")
    
  
    
                        
