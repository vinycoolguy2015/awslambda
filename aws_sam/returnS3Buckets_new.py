import boto3
import json
def lambda_handler(event, context):
	buckets = [bucket.name for bucket in boto3.resource('s3').buckets.all()]
	counter=0
	for bucket in buckets:
	    if bucket.startswith('a'):
	        counter=counter+1
	return {
        'statusCode': 200,
        'body': json.dumps(counter)
    }
