import boto3
import json

QUEUE=''

# Create an SQS client object
sqs = boto3.client('sqs',region_name='ap-southeast-1')


# Get the queue URL
queue_url = sqs.get_queue_url(QueueName=QUEUE)['QueueUrl']

# Retrieve all messages from the queue
messages = []
while True:
    response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10)
    if 'Messages' not in response:
        break
    messages += response['Messages']

# Process the messages
for message in messages:
    data=json.loads(message['Body'])
    event_message=data['event_payload']['message']
    event=json.loads(event_message)
    if event["userIdentity"]["type"] != "AWSService":
        json_data={}
        json_data["eventName"]=event["eventName"]
        json_data["eventSource"]=event["eventSource"]
        json_data["awsRegion"]=event["awsRegion"]
        json_data["eventTime"]=event["eventTime"]
        json_data["userIdentityType"]=event["userIdentity"]["type"]
        json_data["roleAssumedBy"]=event['userIdentity']['principalId']
        json_data["roleAssumed"]=event['userIdentity']['sessionContext']['sessionIssuer']['arn']
        json_formatted_str = json.dumps(json_data, indent=2)
        print(json_formatted_str)
