def lambda_handler(event, context):

	import boto3
	import sys
	
	queueURL='https://sqs.us-east-1.amazonaws.com/<account>/qasnapshot-queue'

	client = boto3.client('sqs')
	#ec2 = boto3.client('ec2')
	response = client.receive_message(QueueUrl=queueURL,MaxNumberOfMessages=3,WaitTimeSeconds=15,VisibilityTimeout=600,MessageAttributeNames =['All'])

	if 'Messages' not in response:
		sys.exit()
	for message in response['Messages']:
		if 'MessageAttributes' not in message:
			response = client.delete_message(QueueUrl=queueURL,ReceiptHandle=message['ReceiptHandle'])
        else:	
			ec2 = boto3.client('ec2',region_name=message['MessageAttributes']['region']['StringValue'])
			response = ec2.describe_snapshots(SnapshotIds=[message['MessageAttributes']['snapshotid']['StringValue']])
			if response['Snapshots'][0]['State']=='completed':
				print ("Copying the snapshot to Singapore region")
				conn = boto3.client('ec2',region_name='ap-southeast-1')
				response=conn.copy_snapshot(SourceRegion=message['MessageAttributes']['region']['StringValue'], SourceSnapshotId=message['MessageAttributes']['snapshotid']['StringValue'])
				conn.create_tags(Resources=[response['SnapshotId']],Tags=[{'Key': 'Name', 'Value':message['MessageAttributes']['snapshotname']['StringValue'] },
                                        {'Key': 'Instance_ID', 'Value':message['MessageAttributes']['instanceid']['StringValue']},
                                         {'Key': 'ProdAuth-DeleteOn', 'Value':message['MessageAttributes']['deleteon']['StringValue']}])
				response = client.delete_message(QueueUrl=queueURL,ReceiptHandle=message['ReceiptHandle']) 
    			print response
