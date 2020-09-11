import boto3 
import csv

filePath ='instance_details.csv'
REGIONS = [
		'eu-west-1',
		'ap-northeast-1',
		'us-east-1',
		] 
		
csv_file = open(filePath,'w+')
csv_file.write("Region,InstanceId,InstanceName,InstanaceState,LaunchTime,InstanceType,Key,VPCId,SubnetId,PublicIp,PrivateIp,SecurityGroup\n\n")

for region in REGIONS:
	client = boto3.client('ec2',region_name=region)
	response = client.describe_instances()
	for reservation in response['Reservations']:
		for instance in reservation['Instances']:
			if instance['State']['Name'] in ['stopped','running']:
				instancename = ''
				if 'Tags' in instance:
					for tags in instance['Tags']:
						if tags["Key"] == 'Name':
							instancename = tags["Value"]
				public_ip=[]
				private_ip=[]
				security_groups=[]
				for NetworkInterface in instance['NetworkInterfaces']:
					for ip in NetworkInterface['PrivateIpAddresses']:
						if 'Association' in ip:
							public_ip.append(ip['Association']['PublicIp'])
						private_ip.append(ip['PrivateIpAddress'])
				
				for security_group in instance['SecurityGroups']:
					security_groups.append(security_group['GroupId'])
				
				csv_file.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(
								region,
								instance['InstanceId'],
								instancename,
								instance['State']['Name'],
								str(instance['LaunchTime']),
								instance['InstanceType'],
								instance['KeyName'],
								instance['VpcId'],
								instance['SubnetId'],
								(';'.join(public_ip)),
								(';'.join(private_ip)),
								(';'.join(security_groups))
				
							))
				csv_file.flush() 
				
