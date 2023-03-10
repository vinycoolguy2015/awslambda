import boto3

client = boto3.client('cloudwatch')
sns='arn:aws:sns:us-east-1:808399:patching'

response = client.put_composite_alarm(
    ActionsEnabled=True,
    AlarmActions=[
        sns,
    ],
    AlarmDescription='Test Alarm',
    AlarmName='Test Alarm',
    AlarmRule='ALARM(Web_Server_CPU_Utilization) AND ALARM(glue_access_denied)'
    
   
)
