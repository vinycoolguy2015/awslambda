import boto3
import json
import gzip
import os
import logging
import urllib.request

s3_bucket="<S3_BUCKET_NAME>"
s3_client = boto3.client('s3',region_name='us-east-1')

logger = logging.getLogger()

appconfig_url = f'http://localhost:2772/applications/CloudTrail/environments/Dev/configurations/CloudTrail'
config = json.loads(urllib.request.urlopen(appconfig_url).read())
APIS_TO_TRACK=config['APIS_TO_TRACK']

def lambda_handler(event, context):
    s3_objects=[]
    for event_records in event['Records']:
        event_body=json.loads(event_records['body'])
        for record in event_body['Records']:
            s3_object=record['s3']['object']['key']
            if s3_object not in s3_objects:
                s3_objects.append(s3_object)
    
    for object in s3_objects:
        s3_client.download_file(s3_bucket,object,'/tmp/s3_object.gz')
        with gzip.open('/tmp/s3_object.gz', 'rb') as gzipped_file:
            gzipped_content = gzipped_file.read()
            json_string = gzipped_content.decode('utf-8')
            json_object = json.loads(json_string)
            if 'Records' in json_object:
                for message in json_object['Records']:
                    if message["userIdentity"]["type"] != "AWSService":
                        found = False
                        for api_call in APIS_TO_TRACK:
                            if ({"EventSource": api_call["EventSource"],"EventName": api_call["EventName"]} == {"EventSource": message["eventSource"],"EventName": message["eventName"]}) and message["userIdentity"]["arn"] not in api_call['User']:
                                found = True
                                logger.info("CloudTrail API Call logged",  extra={"User": message["userIdentity"]["arn"],"EventTime": message["eventTime"],"EventSource": message["eventSource"],"EventName": message["eventName"],"Region": message["awsRegion"],"IP": message["sourceIPAddress"] })
                                break
                            
                        
        os.remove('/tmp/s3_object.gz')
