import boto3

inspector = boto3.client('inspector2',region_name='ap-southeast-1')

exempted_cves=['CWE-319','CWE-117','CWE-93']
exempted_functions=['lambda1','lambda2']

# Create a reusable Paginator
paginator = inspector.get_paginator('list_findings')

# Create a PageIterator from the Paginator
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
                    print(finding['title'])
                    print(resource['id'])
                    print(resource['details']['awsLambdaFunction']['functionName'])
                    print("-------")
