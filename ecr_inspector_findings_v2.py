import boto3
import json
ecr_repo_list=['repoA','repoB']
jmespath_expression = 'sort_by(imageDetails, &to_string(imagePushedAt))[-1].imageTags'
client = boto3.client('ecr',region_name='ap-southeast-1')
sns_client = boto3.client('sns',region_name='ap-southeast-1')
paginator = client.get_paginator('describe_images')

def lambda_handler(event, context):
   for ecr_repo_name in ecr_repo_list:
        high_severity_vulns=0
        critical_severity_vulns=0
        iterator = paginator.paginate(repositoryName=ecr_repo_name,maxResults=1000,)
        filter_iterator = iterator.search(jmespath_expression)
        latest_image_tag = list(filter_iterator)[0]
        latest_image_scan_result = client.describe_image_scan_findings(repositoryName=ecr_repo_name,imageId={'imageTag': latest_image_tag})
        vuln_status=latest_image_scan_result['imageScanFindings']['findingSeverityCounts']
        if 'HIGH' in vuln_status:
                high_severity_vulns=vuln_status['HIGH']
        if 'CRITICAL' in vuln_status:
                critical_severity_vulns=vuln_status['CRITICAL']
        if(high_severity_vulns > 0 or critical_severity_vulns > 0):
                #print(ecr_repo_name+":"+latest_image_tag+" image contains "+str(critical_severity_vulns)+" critical and "+str( high_severity_vulns)+" high severity vulnerabilities")
                message = {"version": "1.0","source": "custom","content": {
        "description": ecr_repo_name+":"+latest_image_tag+" image contains "+str(critical_severity_vulns)+" critical and "+str( high_severity_vulns)+" high severity vulnerabilities"}}
                #message=ecr_repo_name+":"+latest_image_tag+" image contains "+str(critical_severity_vulns)+" critical and "+str( high_severity_vulns)+" high severity vulnerabilities"
                response = sns_client.publish(TargetArn='arn:aws:sns:ap-southeast-1:091308437569:ecr_scan_findings',
                                Message=json.dumps({'default': json.dumps(message)}),
                                MessageStructure='json')
