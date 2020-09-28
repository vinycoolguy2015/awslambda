import boto3
from botocore.exceptions import ClientError

ACCESS_KEY=''
SECRET_ACCESS_KEY=''
REGION='ap-south-1'

ec2client = boto3.client('ec2',aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_ACCESS_KEY,region_name=REGION)
instances=[]
response = ec2client.describe_instances()
print "Select the instance from the list"
print "---------------------------------"
for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        for tag in instance['Tags']:
            if tag['Key'] == 'Name':
                data={}
                instance_name=tag['Value']
                instance_id=instance["InstanceId"]
                data['instance_name']=instance_name
                data['instance_id']=instance_id
                instances.append(data)
                print instance_name
print ("------------------------")
instance=raw_input("Select instance:")
instance_id=(item for item in instances if item["instance_name"] == instance).next()['instance_id']
response = ec2client.describe_instances(InstanceIds=[instance_id])
security_groups=response['Reservations'][0]['Instances'][0]['SecurityGroups']
if len(security_groups) > 1:
    print "This instance has multiple security groups assigned.Please select the group you want to update"
    print "---------------------------------------"
    for security_group in security_groups:
        print security_group['GroupName']
    print "-------------------"
    group=raw_input("Select security group:")
    security_group_id=(item for item in security_groups if item["GroupName"] == group).next()['GroupId']
else:
   security_group_id= security_groups[0]['GroupId']
print "---------------------"
port=int(raw_input("Enter port number you want to revoke access to:"))
ip=raw_input("Enter IP with /32 suffix you want to revoke access from:")

try:
    response = ec2client.revoke_security_group_ingress(GroupId=security_group_id,
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': port,
             'ToPort': port,
             'IpRanges': [{'CidrIp': ip}]}
        ])
except ClientError as e:
    print(e)
else:
    print ("Access revoked")
