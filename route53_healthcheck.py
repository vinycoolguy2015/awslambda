import boto3
import string
import random

route53_client = boto3.client('route53')
cloudwatch_client = boto3.client('cloudwatch')

sns_arn=''

websites=['www.bbc.com','www.espncricinfo.com']
for website in websites:
    print("Creating health check for "+website)
    response = route53_client.create_health_check(
        CallerReference=''.join(random.sample(string.ascii_lowercase, 9)),
        HealthCheckConfig={
            'Type': 'HTTPS',
            'FullyQualifiedDomainName': website,
            'RequestInterval': 30,
            'FailureThreshold': 2,
            'MeasureLatency': True,
            'Regions': [
                'ap-southeast-1', 'ap-southeast-2', 'us-east-1',
            ]
        }
    )
    
    route53_client.change_tags_for_resource(
        ResourceType='healthcheck',
        ResourceId=response['HealthCheck']['Id'],
        AddTags=[
            {
                'Key': 'Name',
                'Value': website
            }
        ]
    )
    
    cloudwatch_client.put_metric_alarm(
        AlarmName=website,
        ComparisonOperator='LessThanThreshold',
        EvaluationPeriods=2,
        MetricName='HealthCheckStatus',
        Namespace='AWS/Route53',
        Dimensions=[{'Name': 'HealthCheckId', 'Value': response['HealthCheck']['Id']}],
        Period=60,
        Statistic='Average',
        Threshold=1,
        ActionsEnabled=True,
        AlarmActions=[sns_arn],
        AlarmDescription='Notify when a health check fails', Unit='Seconds')
