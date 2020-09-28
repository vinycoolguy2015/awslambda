#Create a FIFO Queue
import boto3

# Create SQS client
sqs = boto3.client('sqs')

# Create a SQS queue
response = sqs.create_queue(
    QueueName='mynewq.fifo',
    Attributes={
        'DelaySeconds': '5',
        'MessageRetentionPeriod': '86400',
        'FifoQueue': 'true',
        'ContentBasedDeduplication': 'true'
    }
)

print(response['QueueUrl'])

#Create producer
import boto3
import json
import time
from sqs_url import QUEUE_URL

# Create SQS client
sqs = boto3.client('sqs')

with open('data.json', 'r') as f:
    data = json.loads(f.read())

for i in data:
    msg_body = json.dumps(i)
    response = sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=msg_body,
        MessageAttributes={
            'JobType': {
                'DataType': 'String',
                'StringValue': 'NewDonor'
            },
            'Producer': {
                'DataType': 'String',
                'StringValue': 'Default'
            }
        },
        MessageGroupId='messageGroup1'
    )
    print("Added Message:")
    print(response)
    time.sleep(1)

	
# Create consumer
import boto3
import json
import time
from sqs_url import QUEUE_URL

# Create SQS client
sqs = boto3.client('sqs')

i = 0

while i < 10000:
    i = i + 1
    rec_res = sqs.receive_message(
        QueueUrl=QUEUE_URL,
        MessageAttributeNames=[
            'All',
        ],
        MaxNumberOfMessages=1,
        VisibilityTimeout=5,
        WaitTimeSeconds=10
    )
    time.sleep(2)
    # If our task takes too long we can't delete it
    # time.sleep(5)
    del_res = sqs.delete_message(
        QueueUrl=QUEUE_URL,
        ReceiptHandle=rec_res['Messages'][0]['ReceiptHandle']
    )
    print("RECIEVED MESSAGE:")
    print('FROM PRODUCER: ' + rec_res['Messages'][0]['MessageAttributes']['Producer']['StringValue'])
    print('JOB TYPE: ' + rec_res['Messages'][0]['MessageAttributes']['JobType']['StringValue'])
    print('BODY: ' + rec_res['Messages'][0]['Body'])
    print("DELETED MESSAGE")
    print("")
    time.sleep(1)
	
	
#Purge a queue
import boto3
from sqs_url import QUEUE_URL

sqs = boto3.client('sqs')

response = sqs.purge_queue(
    QueueUrl=QUEUE_URL
)
