import json
import boto3
import os 
import re

ses_client=boto3.client("ses")

def lambda_handler(event, context):
   CreatedDate= event['detail']['responseElements']['user']['createDate']
   Username = event['detail']['responseElements']['user']['userName']
   CreatedBy=''
   if event['detail']['userIdentity']['type']=='IAMUser':
      CreatedBy=event['detail']['userIdentity']['userName']
   elif event['detail']['userIdentity']['type']=='AssumedRole':
      CreatedBy=event['detail']['userIdentity']['principalId']
   pattern = '^d'
   result = re.match(pattern,Username.lower().strip())
   if not result:
      if CreatedBy=='':
         Data=' User ' +Username + ' got created on ' + CreatedDate
      else:
         Data=' User ' +Username + ' got created on ' + CreatedDate + ' by '+CreatedBy
      print(Data)    
      send_email("IAM Notification",Data)
   
def send_email(subject,body):
    ses_client.send_email(Source=os.environ['Source'],Destination={'ToAddresses': [os.environ['Recipient']]},
    Message={
        'Subject': {
            'Data': subject
        },
        'Body': {
            'Text': {
                'Data': body
            }
        }
    }
)
