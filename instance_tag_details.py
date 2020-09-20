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
		'us-west-2' ] 
for region in REGIONS:
    client = boto3.client('ec2',region_name=region)
    response = client.describe_instances()
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            if instance['State']['Name'] in ['stopped','running']:
                instancename = ''
				BASELINE_ID=''
				BILLING_COMPANY=''
				BILLING_CREATEDBY=''
				BILLING_END_DATE=''
				BILLING_ENVIRONMENT=''
				
        if 'Tags' in instance:
            for tags in instance['Tags']:
                if tags["Key"] == 'Name':
                    instancename = tags["Value"]
				if tags["Key"]=='BASELINE_ID':
				    BASELINE_ID=tags["Value"]
				if tags["Key"]=='BILLING_COMPANY':
                    BILLING_COMPANY=tags["Value"]
				if tags["Key"]=='BILLING_CREATEDBY':
                    BILLING_CREATEDBY=tags["Value"]
				if tags["Key"]=='BILLING_END_DATE':
                    BILLING_END_DATE=tags["Value"]
				if tags["Key"]=='BILLING_ENVIRONMENT':
                    BILLING_ENVIRONMENT=tags["Value"]	
                                
                                                                       
        print region+','+instance['InstanceId']+','+instancename+','+instance['State']['Name']+','+BASELINE_ID+','+BILLING_COMPANY+','+BILLING_CREATEDBY+','+BILLING_END_DATE+','+BILLING_ENVIRONMENT
