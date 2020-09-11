  1 import boto3
  2 from botocore.exceptions import ClientError
  3
  4 ec2 = boto3.client('ec2',region_name='ap-south-1')
  5
  6 try:
  7         response = ec2.describe_security_groups(GroupIds=['sg-008e346b'])
  8         rules=response['SecurityGroups'][0]['IpPermissions']
  9         number_of_rules=len(response['SecurityGroups'][0]['IpPermissions'])
 10         for rule in rules:
 11                 port=rule['FromPort']
 12                 for ip in rule['IpRanges']:
 13                         cidr=ip['CidrIp']
 14                         print port,cidr
 15                 for groups in rule['UserIdGroupPairs']:
 16                         group=groups['GroupId']
 17                         print port,group
 18 except ClientError as e:
 19         print(e)
