import boto3
import os
import csv

def lambda_handler(event, context):
    asg_client = boto3.client('autoscaling')
    s3 = boto3.client('s3')
    ec2_client = boto3.client('ec2')
    
    asg =   "WebServerGroup"
    filename=''
    
    asg_response = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg])
    instance_ids = [] # List to hold the instance-ids

    for i in asg_response['AutoScalingGroups']:
        for k in i['Instances']:
            instance_ids.append(k['InstanceId'])
    
    ec2_response = ec2_client.describe_instances(InstanceIds = [instance_ids[0]]) 
    if 'Tags' in ec2_response['Reservations'][0]['Instances'][0]:
        for tags in ec2_response['Reservations'][0]['Instances'][0]['Tags']:
            if tags["Key"] == 'Role':
                role = tags["Value"]
    
    filename="unique_id_"+role+'_'+os.environ['AWS_REGION']
    
    s3.download_file(<bucketname>, filename, "/tmp/"+filename)
    
    with open("/tmp/"+filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for instance in instance_ids:
            for row in readCSV:
                reservations = ec2_client.describe_instances(Filters=[{'Name':'tag:UNIQUE_ID','Values':[row[0]]}])
                if len(reservations["Reservations"]) == 0:
                    ec2_client.create_tags(Resources=[instance],Tags=[{'Key': 'UNIQUE_ID','Value': row[0]}])
                    break

                
        
