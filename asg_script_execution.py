import boto3
import sys
import subprocess
from ec2_metadata import ec2_metadata

if len(sys.argv) !=2:
  print("Please specify script to be executed")
  sys.exit(0)

client = boto3.client('autoscaling',region_name='us-east-1')
instance_id=ec2_metadata.instance_id
asg_details = client.describe_auto_scaling_instances(InstanceIds=[instance_id])

#print(asg_details)
autoscaling_group_name=asg_details['AutoScalingInstances'][0]['AutoScalingGroupName']

instance_details = client.describe_auto_scaling_groups(AutoScalingGroupNames=[autoscaling_group_name])
instances = [ instance['InstanceId'] for instance in instance_details['AutoScalingGroups'][0]['Instances'] ]
if min(instances) == instance_id.encode('ascii'):
   subprocess.call(['sh',sys.argv[1]])
