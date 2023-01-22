import boto3
import json
def lambda_handler(event, context):
	buckets = [bucket.name for bucket in boto3.resource('s3').buckets.all()]
	return {
        'statusCode': 200,
        'body': json.dumps(len(buckets))
    }
