import boto3


def lambda_handler(event, context):
    instances=[]
    client = boto3.client('ec2')
    instancedata = client.describe_instances()
    for reservation in instancedata['Reservations']:
        if len(reservation['Instances']) >0:
            for instance in reservation['Instances']:
                instancedetails={}
                instancename="Unnamed Instance"
                instancedeletiondate="None"
                if 'Tags' in instance:
                    for tags in instance['Tags']:
                        if tags["Key"] == 'Name':
                            instancedetails['instancename'] = tags["Value"]
                    for tags in instance['Tags']:
                        if tags["Key"] == 'Delete_On':
                            instancedetails['instancedeletiondate']=tags["Value"]
                instances.append(instancedetails)
                            
    return instances
            
