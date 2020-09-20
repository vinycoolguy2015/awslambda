import boto3
import json

def lambda_handler(event, context):
    
    ec2info = {}
    region=event['region']
    instance_id=event['detail']['instance-id']
    instance_state=event['detail']['state']
    Name=""
    BILLING_COMPANY=""
    BILLING_ENVIRONMENT=""
    BILLING_JIRA=""
    BILLING_REGION=""
    #pvt_ip=""
    ec2 = boto3.client('ec2', region_name = region)
    ses = boto3.client('ses',region_name='us-east-1')
    response = ec2.describe_instances(InstanceIds=[instance_id])
    if 'Tags' in response['Reservations'][0]['Instances'][0]:
        for tags in response['Reservations'][0]['Instances'][0]['Tags']:
            if tags["Key"] == 'Name':
                Name = tags["Value"]
            if tags["Key"] == 'BILLING_COMPANY':
                BILLING_COMPANY = tags["Value"]
            if tags["Key"] == 'BILLING_ENVIRONMENT':
                BILLING_ENVIRONMENT = tags["Value"]
            if tags["Key"] == 'BILLING_JIRA':
                BILLING_JIRA = tags["Value"]
            if tags["Key"] == 'BILLING_REGION':
                BILLING_REGION = tags["Value"]
                #pvt_ip = response["Reservations"][0]["Instances"][0]["PrivateIpAddress"]
                
    ec2info['Name']=Name
    ec2info['InstanceID']=instance_id
    #ec2info['PRIVATE_IP']=pvt_ip
    ec2info['BILLING_ENVIRONMENT']=BILLING_ENVIRONMENT
    ec2info['BILLING_COMPANY']=BILLING_COMPANY
    ec2info['BILLING_JIRA']=BILLING_JIRA
    ec2info['BILLING_REGION']=BILLING_REGION
    ec2info['State']=instance_state
    ec2info['Time']=event['time']
    ses.send_email(Source='term_notify@abc.net',Destination={'ToAddresses': ["monitoringteam@abc.net"]},
    
    Message={
        'Subject': {
            'Data': 'EC2 - Termination Alert'
        },
        'Body': {
            'Text': {
                'Data': json.dumps(ec2info, indent=4)
            }
        }
    }
)
