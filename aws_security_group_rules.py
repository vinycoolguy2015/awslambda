# Script to check security group rules for all the instances in a region. 
#Provide your access_key,secret_access_key and region name before running the script.


import boto3
from botocore.exceptions import ClientError
from prettytable import PrettyTable
table = PrettyTable(['Instance','Security_Group_Name','Port', 'Ingress_Allowed'])
client = boto3.resource(
    'ec2',
    aws_access_key_id='',
    aws_secret_access_key='',
    region_name=''
)
instances = client.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
security_groups=[]
for instance in instances:
    for security_group in instance.security_groups:
       if security_group not in security_groups:
          security_groups.append(security_group)
for security_group in security_groups:
    group_name=security_group['GroupName']
    security_group_permissions = client.SecurityGroup(security_group['GroupId']).ip_permissions
    instances = client.instances.filter(Filters=[{'Name': 'instance.group-id', 'Values': [client.SecurityGroup(security_group['GroupId']).id]}])
    sg_instances=[]
    inst_names = [tag['Value'] for i in instances for tag in i.tags if tag['Key'] == 'Name']
    for security_group_permission in security_group_permissions:
        permissions=[]
        if security_group_permission['IpProtocol']== '-1':
            port='ALL'
            for ip in security_group_permission['IpRanges']:
                permissions.append(ip['CidrIp'])
            for sg in security_group_permission['UserIdGroupPairs']:
                permissions.append(sg['GroupId'])
        else:
            port=security_group_permission['FromPort']
            for ip in security_group_permission['IpRanges']:
                permissions.append(ip['CidrIp'])
            for sg in security_group_permission['UserIdGroupPairs']:
                permissions.append(sg['GroupId'])


        table.add_row([inst_names,group_name,port, permissions])
        
  print table
