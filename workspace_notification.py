import boto3
import os 
from datetime import datetime


workspace_client = boto3.client("workspaces")
ses_client=boto3.client("ses")

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

def workspace_usage(directoryid):
    marker = None
    records=[]
    while True:
        paginator = workspace_client.get_paginator('describe_workspaces')
        response_iterator = paginator.paginate( DirectoryId=directoryid,PaginationConfig={'MaxItems': 25,'StartingToken': marker})
        for page in response_iterator:
            for workspace in page['Workspaces']:
                workspace_detail = workspace_client.describe_workspaces_connection_status(WorkspaceIds=[workspace['WorkspaceId']])
                workspaceid=workspace['WorkspaceId']
                workspaceusername=workspace['UserName']
                if 'LastKnownUserConnectionTimestamp' in workspace_detail['WorkspacesConnectionStatus'][0]:
                    workspacelastuseddate=workspace_detail['WorkspacesConnectionStatus'][0]['LastKnownUserConnectionTimestamp']
                    time_difference=datetime.utcnow()-workspacelastuseddate.replace(tzinfo=None)
                    if (time_difference.total_seconds() / (3600*24)) > 90:
                        records.append("Workspace "+workspaceid+" belongs to "+workspaceusername+" which was last used on "+str(workspacelastuseddate.date()))
                else:
                     records.append("Workspace "+workspaceid+" belongs to "+workspaceusername+" and we do not have info about the date it was last used on ")
                    
        try:
            marker = page['NextToken']
        except KeyError:
            break
    return records
            

def lambda_handler(event, context):
    
    directories=['d-xyz','d-123']
    workspace_notifications=[]
    
    for directory in directories:
        data=workspace_usage(directory)
        workspace_notifications=workspace_notifications+data
    
    if len(workspace_notifications) > 0:
        send_email("Workspace Notification",'\n\n'.join(workspace_notifications))
        
        
        
    
    
    


    





    
    
    


    

