import boto3
import os
import json
from botocore.exceptions import ClientError

s3_client = boto3.client('s3')
cloudfront_client = boto3.client('cloudfront')
s3_control_client = boto3.client('s3control')
iam_client = boto3.client('iam')

def lambda_handler(event, context):
    
    #Create Folder in S3
    tenant=event['queryStringParameters']['tenant']
    bucket_name = os.environ['S3_BUCKET']
    try:
        s3_client.put_object(Bucket=bucket_name, Key=(tenant+'/'))
    except ClientError as e:
        print(e.response)
        return {
            'statusCode': 500,
            'body': json.dumps('Error Creating S3 Folder')
        }
    
    #Create S3 Access Point
    try:
        response = s3_control_client.create_access_point(
            AccountId= event['requestContext']['accountId'], #context.invoked_function_arn.split(":")[4],
            Name=tenant,
            Bucket=os.environ['S3_BUCKET'],
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            }
        )
    except ClientError as e:
        print(e.response)
        return {
            'statusCode': 500,
            'body': json.dumps('Error Creating S3 Access Point')
        }
        
    #Create S3 Access Point Policy
    policy_doc = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:PutObject"
                ],
                "Resource": "arn:aws:s3:us-east-1:"+event['requestContext']['accountId']+":accesspoint/"+tenant+"/object/"+tenant+"/*"
            }
        ]
    }

   
    policy_doc_json = json.dumps(policy_doc)
    try:
        response = iam_client.create_policy(PolicyName=tenant,PolicyDocument=policy_doc_json)
        iam_client.attach_role_policy(RoleName=os.environ['ROLE_NAME'], PolicyArn=response['Policy']['Arn'])
    except ClientError as e:
        print(e.response)
        return {
            'statusCode': 500,
            'body': json.dumps('Error Creating S3 Access Point Policy')
        }
        
    #Update CloudFront
    distribution_id = os.environ["CLOUDFRONT_DISTRIBUTION_ID"]
    response = cloudfront_client.get_distribution_config(Id=distribution_id)

    new_origin_config = {
        'Id': tenant,
        'DomainName': os.environ['S3_DOMAIN_NAME'],
        'S3OriginConfig': {
            'OriginAccessIdentity': ''
        },
        'OriginPath' : "/"+tenant,
        'CustomHeaders' : {'Quantity':0}
    }
    response['DistributionConfig']['Origins']['Items'].append(new_origin_config)
    response['DistributionConfig']['Origins']['Quantity'] += 1


    new_behavior_config = {
        'PathPattern': "/"+tenant+"/*",
        'TargetOriginId': tenant,
        'ViewerProtocolPolicy': 'redirect-to-https',
        'SmoothStreaming': False,
        "Compress": True,
        "CachePolicyId": "658327ea-f89d-4fab-a63d-7e88639e58f6",
        "FieldLevelEncryptionId": "",
        "AllowedMethods": {
                "Quantity": 2,
                "Items": ["HEAD", "GET"],
                "CachedMethods": {
                        "Quantity": 2,
                        "Items": ["HEAD", "GET"]
                }
            },
        "LambdaFunctionAssociations": {
                "Quantity": 0
            },
        "FunctionAssociations": {
                "Quantity": 0
            },
        }

    if 'Items' not in response['DistributionConfig']['CacheBehaviors']:
        response['DistributionConfig']['CacheBehaviors']['Items']=[]
    response['DistributionConfig']['CacheBehaviors']['Items'].append(new_behavior_config)
    response['DistributionConfig']['CacheBehaviors']['Quantity'] += 1

    try:
        cloudfront_client.update_distribution(
            DistributionConfig=response['DistributionConfig'],
            Id=distribution_id,
            IfMatch=response['ETag']
        )
    except ClientError as e:
        print(e.response)
        return {
            'statusCode': 500,
            'body': json.dumps('Error Creating CloudFront Origin')
        }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps('Tenant onboarded successfully')
        }
