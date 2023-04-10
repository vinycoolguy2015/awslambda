import boto3
cloudwatch_client_us = boto3.client('logs',region_name='us-east-1')
cloudwatch_client=boto3.client('logs',region_name='ap-southeast-1')
response = cloudwatch_client_us.describe_log_groups(logGroupNamePrefix='/aws/lambda/')
for log_group in response['logGroups']:
    print(log_group['logGroupName'])
    cloudwatch_client_us.put_retention_policy(logGroupName=log_group['logGroupName'],retentionInDays=90)
response = cloudwatch_client.describe_log_groups(logGroupNamePrefix='/aws/lambda/')
for log_group in response['logGroups']:
    print(log_group['logGroupName'])
    cloudwatch_client.put_retention_policy(logGroupName=log_group['logGroupName'],retentionInDays=90)
