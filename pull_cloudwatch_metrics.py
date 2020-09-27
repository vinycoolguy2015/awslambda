#####Instance CPUUtilization

import boto3
aws_access_key_id=""
aws_secret_access_key=""

ec2_client = boto3.client('autoscaling',region_name='eu-west-1')
cloudwatch_client = boto3.client('cloudwatch',region_name='eu-west-1')


response = ec2_client.describe_auto_scaling_groups(
    AutoScalingGroupNames=[
        'RevProxyAutoScalingGroup'
    ]
)
instances=response['AutoScalingGroups'][0]['Instances']
for instance in instances:
    response = cloudwatch_client.get_metric_statistics(
    Namespace='AWS/EC2',
    MetricName='CPUUtilization',
    Dimensions=[
        {
            'Name': 'InstanceId',
            'Value': instance['InstanceId']
        },
    ],
    StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=3600),
    EndTime=datetime.datetime.utcnow(),
    Period=3600,
    Statistics=[
        'Maximum',
    ],
    
    Unit='Percent'
)
    print (nstance['InstanceId'],response['Datapoints'][0]['Maximum'])

	
	
####Load Balancer Request Count
import boto3

cloudwatch_client = boto3.client('cloudwatch',region_name='eu-west-1')

response = cloudwatch_client.get_metric_statistics(
    Namespace='AWS/ELB',
    MetricName='RequestCount',
    Dimensions=[
        {
            'Name': 'LoadBalancerName',
            'Value': 'ElasticL-Y06S8VDPDCL8'
        },
    ],
    StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=3600),
    EndTime=datetime.datetime.utcnow(),
    Period=3600,
    Statistics=[
        'Sum',
    ],
    
    Unit='Count'
)


###Load Balancer Latency
import boto3

cloudwatch_client = boto3.client('cloudwatch',region_name='eu-west-1')

response = cloudwatch_client.get_metric_statistics(
    Namespace='AWS/ELB',
    MetricName='Latency',
    Dimensions=[
        {
            'Name': 'LoadBalancerName',
            'Value': 'ElasticL-Y06S8VDPDCL8'
        },
    ],
    StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=3600),
    EndTime=datetime.datetime.utcnow(),
    Period=3600,
    Statistics=[
        'Average',
    ],
    
    Unit='Seconds'
)

##RDS CPUUtilization
import boto3

cloudwatch_client = boto3.client('cloudwatch',region_name='eu-west-1')

response = cloudwatch_client.get_metric_statistics(
    Namespace='AWS/RDS',
    MetricName='CPUUtilization',
    Dimensions=[
        {
            'Name': 'DBInstanceIdentifier',
            'Value': 'prod-2'
        },
    ],
    StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=3600),
    EndTime=datetime.datetime.utcnow(),
    Period=3600,
    Statistics=[
        'Average',
    ],
    
    Unit='Percent'
)

##RDS Request Count
import boto3

cloudwatch_client = boto3.client('cloudwatch',region_name='eu-west-1')

response = cloudwatch_client.get_metric_statistics(
    Namespace='AWS/RDS',
    MetricName='DatabaseConnections',
    Dimensions=[
        {
            'Name': 'DBInstanceIdentifier',
            'Value': 'prod-2'
        },
    ],
    StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=3600),
    EndTime=datetime.datetime.utcnow(),
    Period=3600,
    Statistics=[
        'Average',
    ],
    
    Unit='Count'
)



	
