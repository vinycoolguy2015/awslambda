from pymongo import MongoClient
import sys
import boto3
import re

def send_email(subject,text,source,recipient):
    client=boto3.client('ses')
    client.send_email(Destination={'ToAddresses': [recipient]},
                Message={
                'Body': {
            'Text': {
                'Charset': 'UTF-8',
                'Data': text,
            },
        },
        'Subject': {
            'Charset': 'UTF-8',
            'Data': subject,
        },
    },
    Source=source,
)

def lambda_handler(event, context):
    
    MONGO_DB = "admin"
    desired_member_count=7
    email_subject="Prod_Mongo_Monitoring_Alert"
    email_source="prod_mongo_monitoring@abc.net"
    email_recipient="vinayak@abc.com"
    pattern = '^use1'
  
   
    
    #connection = MongoClient(MONGO_HOST, MONGO_PORT)
    connection=MongoClient("mongodb://172.25.4.xyz:27017,172.25.4.xyz:27017,172.25.4.xyz:27017/?replicaSet=rs_36")
    db = connection[MONGO_DB]
    replicaset_status=db.command("replSetGetStatus")
    
    if len( replicaset_status['members'])  != desired_member_count:
        send_email(email_subject,"Replicaset does not have sufficient members",email_source,email_recipient)
    
    for member in replicaset_status['members']:
        if member['stateStr'] == 'PRIMARY':
            result = re.match(pattern,member['name'].lower().strip())
            if not result:
                send_email(email_subject, "Prod Mongo Primary is not is US region.Please take the corrective action immediately ",email_source,email_recipient)
            else:
                print("Mongo Primary is in US region")
        if member['health'] != 1 or member['state'] not in [1,2,7]:
            send_email(email_subject, member['name']+" is having some issues.",email_source,email_recipient)
           
            
