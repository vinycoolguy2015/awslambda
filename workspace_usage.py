import boto3
from datetime import datetime


cloudwatch_client = boto3.client('cloudwatch')
workspace_client = boto3.client("workspaces")

directories=['','']
for directory in directories:
    marker = None
    records=[]
    while True:
        paginator = workspace_client.get_paginator('describe_workspaces')
        response_iterator = paginator.paginate( DirectoryId=directory,PaginationConfig={'MaxItems': 25,'StartingToken': marker})
        for page in response_iterator:
            for workspace in page['Workspaces']:
                #print("Fetching data for "+workspace['WorkspaceId'])
                count = 0
                for day in range(1,31):
                    workspace_used=0
                    workspace_reused=0
                    response = cloudwatch_client.get_metric_statistics(Namespace="AWS/WorkSpaces",MetricName="UserConnected",Dimensions=[{'Name': 'WorkspaceId','Value': workspace['WorkspaceId']}],StartTime=datetime(2019,12,day),EndTime=datetime(2019,12,day+1),Period=300,Statistics=['Average'])
                    for data in sorted(response['Datapoints'], key = lambda i: i['Timestamp']):
                        if data['Average'] > 0:
                            if workspace_used==0:
                                workspace_used=1
                                count=count-1
                            elif workspace_used==1 and workspace_reused==0:
                                #print("Workspace "+ workspace['WorkspaceId']+" reused during sameday on "+str(day))
                                count=count-1
                            count=count+1
                        else:
                            workspace_reused=1
                print("Workspace "+workspace['WorkspaceId']+" used for " +str(count/12) +" hours")
                
                    
        try:
            marker = page['NextToken']
        except KeyError:
            break
    

