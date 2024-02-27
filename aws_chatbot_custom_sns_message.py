import json
import boto3

message = {"version": "1.0","source": "custom","content": {
        "description": "Test"}}
client = boto3.client('sns',region_name='ap-southeast-1')
response = client.publish(
    TargetArn='arn:aws:sns:ap-southeast-1:093052954960:ecr_image_scan_findings',
    Message=json.dumps({'default': json.dumps(message)}),
    MessageStructure='json'
)
