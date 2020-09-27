######################################VPC Details#############################################################
import boto3
from prettytable import PrettyTable
table = PrettyTable(['Region','VPC Id','VPC Name','VPC CIDR'])

REGIONS = [
    'us-east-1',
    'eu-west-1',
    'ap-northeast-1'
]
for region in REGIONS:
        client = boto3.client('ec2',region_name=region)
        response = client.describe_vpcs()
        for vpc in response['Vpcs']:
           vpcId=vpc['VpcId']
           vpcCidr=vpc['CidrBlock']
           vpcName=''
           if 'Tags' in vpc:
             vpcName=next(item for item in vpc['Tags'] if item["Key"] == "Name")['Value']
           table.add_row([region,vpcId, vpcName,vpcCidr])
print table

######################################Security Group Details###################################################

import boto3
from prettytable import PrettyTable
table = PrettyTable(['Region','Group Id','Group Name','VPC'])

REGIONS = [
    'us-east-1',
    'eu-west-1	',
    'ap-northeast-1'
]
for region in REGIONS:
        client = boto3.client('ec2',region_name=region)
        response = client.describe_security_groups()
        for SecurityGroup in response['SecurityGroups']:
          table.add_row([region,SecurityGroup['GroupId'],SecurityGroup['GroupName'],SecurityGroup['VpcId']])
print table

######################################Instance Details#########################################################
import boto3
from prettytable import PrettyTable
table = PrettyTable(['Region','InstanceId','ImageId','Instance Type','State'])

REGIONS = [
    'us-east-1',
    'eu-west-1',
    'ap-northeast-1'
]
for region in REGIONS:
        client = boto3.client('ec2',region_name=region)
        Instances=client.describe_instances()['Reservations']

        for instance in Instances:
           state=instance['Instances'][0]['State']['Name']
           instanceId=instance['Instances'][0]['InstanceId']
           imageId=instance['Instances'][0]['ImageId']
           instanceType=instance['Instances'][0]['InstanceType']
           table.add_row([region,instanceId,imageId,instanceType,state])
print (table

############################################################################################
#!/usr/bin/env python

import boto.ec2

for region in [r for r in boto.ec2.regions() if r.name not in ['cn-north-1', 'us-gov-west-1']]:
  conn = boto.ec2.connect_to_region(region.name)
  reservations = conn.get_all_instances()
  for r in reservations:
    for i in r.instances:
      print region.name, i.id,i.state

