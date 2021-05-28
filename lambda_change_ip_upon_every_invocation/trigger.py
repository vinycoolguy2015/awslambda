import boto3
import time

def lambda_handler(event, context):
    client = boto3.client('lambda')
    ec2 = boto3.client('ec2')  
    response = ec2.start_instances(InstanceIds=['i-033aa1badea1496b6']) ## Specify NAT instance ID
    time.sleep(150)
    response = client.invoke(FunctionName='ip')
