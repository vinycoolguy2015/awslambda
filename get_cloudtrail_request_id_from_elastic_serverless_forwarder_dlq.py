import boto3
import json
import gzip

QUEUE='elastic-serverless-forwarder-replay-dlq-1234'
 
# Create an SQS client object
sqs = boto3.client('sqs',region_name='ap-southeast-1')
s3  = boto3.client('s3',region_name='ap-southeast-1')
 
 
# Get the queue URL
queue_url = sqs.get_queue_url(QueueName=QUEUE)['QueueUrl']
 
# Retrieve all messages from the queue
messages = []
s3_bucket=''
s3_objects=[]
request_ids=[]
kibana_query="aws.cloudtrail.request_id: ("
while True:
    response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10)
    if 'Messages' not in response:
        break
    messages += response['Messages']
 
# Process the messages
for message in messages:
    data=json.loads(message['Body'])
    event_message=data['event_payload']['aws']
    #event=json.loads(event_message)
    s3_bucket=event_message['s3']['bucket']['name']
    objectname=event_message['s3']['object']['key']
    if objectname not in s3_objects:
        s3_objects.append(objectname)

for object in s3_objects:
    s3.download_file(s3_bucket,object,'/tmp/s3_object.gz')
    with gzip.open('/tmp/s3_object.gz', 'rb') as gzipped_file:
        gzipped_content = gzipped_file.read()
        json_string = gzipped_content.decode('utf-8')
        json_object = json.loads(json_string)
        for message in json_object['Records']:
            #print(object,message['requestID'])
            request_ids.append(message['requestID'])
            #kibana_query=kibana_query+message['requestID']
kibana_query=kibana_query+' or '.join(request_ids)
kibana_query=kibana_query+")"
print(kibana_query)
print("Total number of failed records "+str(len(request_ids)))
