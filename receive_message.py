#!/usr/bin/env python3

import logging
import time

import boto3
from botocore.exceptions import ClientError
from ec2_metadata import ec2_metadata

QUEUE_NAME = "MyQueue"
AUTOSCALING_GROUP_NAME="MyASG"

logging.basicConfig(format="[%(levelname)s] %(message)s", level="INFO")
sqs = boto3.client("sqs")
autoscaling = boto3.client('autoscaling')

instance_id=ec2_metadata.instance_id
autoscaling.set_instance_protection(InstanceIds=[instance_id],AutoScalingGroupName=AUTOSCALING_GROUP_NAME,ProtectedFromScaleIn=False)


try:
    logging.info(f"Getting queue URL for queue: {QUEUE_NAME}")
    response = sqs.get_queue_url(QueueName=QUEUE_NAME)
except ClientError as e:
    logging.error(e)
    exit(1)

queue_url = response["QueueUrl"]
logging.info(f"Queue URL: {queue_url}")

logging.info("Receiving messages from queue...")

while True:
    messages = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10)
    if "Messages" in messages:
        for message in messages["Messages"]:
            logging.info(f"Message body: {message['Body']}")
            autoscaling.set_instance_protection(InstanceIds=[instance_id],AutoScalingGroupName=AUTOSCALING_GROUP_NAME,ProtectedFromScaleIn=True)
            time.sleep(20)  # simulate work
            sqs.delete_message(
                QueueUrl=queue_url, ReceiptHandle=message["ReceiptHandle"]
            )
            autoscaling.set_instance_protection(InstanceIds=[instance_id],AutoScalingGroupName=AUTOSCALING_GROUP_NAME,ProtectedFromScaleIn=False)

        else:
            logging.info("Queue is now empty")
