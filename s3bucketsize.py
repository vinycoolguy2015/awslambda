import boto3
import datetime

s3 = boto3.client('s3')

for bucket in s3.list_buckets()['Buckets']:
    region=s3.get_bucket_location(Bucket=bucket['Name'])['LocationConstraint']
    if region is None:
        region='us-east-1'
    elif region == 'EU':
        region='eu-west-1'
    
    cloudwatch_client = boto3.client('cloudwatch',region_name=region)
    
    response = cloudwatch_client.get_metric_statistics(Namespace='AWS/S3',MetricName='BucketSizeBytes',Dimensions=[{'Name': 'BucketName','Value': bucket['Name']},{'Name': 'StorageType','Value': 'StandardStorage'}],StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=300),EndTime=datetime.datetime.utcnow(),Period=60,Statistics=['Maximum'])
    
    if len(response['Datapoints']) == 0:
        print(bucket['Name']+','+region+','+'0')
    else:
        print(bucket['Name']+','+region+','+str(response['Datapoints'][0]['Maximum']))
        
