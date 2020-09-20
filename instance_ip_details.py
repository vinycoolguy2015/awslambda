import boto3

REGIONS = [
    'ap-south-1',
		'eu-west-3',
		'eu-west-2',
		'eu-west-1',
		'ap-northeast-2',
		'ap-northeast-1',
		'sa-east-1',
		'ca-central-1',
		'ap-southeast-1',
		'ap-southeast-2',
		'eu-central-1',
		'us-east-1',
		'us-east-2',
		'us-west-1',
		'us-west-2'
]
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
                                for NetworkInterface in instance['NetworkInterfaces']:
                                        for ip in NetworkInterface['PrivateIpAddresses']:
                                                if 'Association' in ip:
                                                        public_ip.append(ip['Association']['PublicIp'])
						print region,instance['InstanceId'],instancename,instance['State']['Name'],public_ip
