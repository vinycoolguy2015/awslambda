import boto3


def lambda_handler(event, context):
    client = boto3.client('ec2')
    codepipeline_client=boto3.client('codepipeline')
    custom_filter = [{'Name':'tag:Name', 'Values': ['WebServer']}]
    
    response = client.describe_instances(Filters=custom_filter)
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id=instance['InstanceId']
            response = client.describe_instance_status(InstanceIds=[instance_id])
            if response['InstanceStatuses'][0]['InstanceState']['Name'] == 'running':
                codepipeline_client.put_job_success_result(jobId=event['CodePipeline.job']['id'])
            else:
                response = codepipeline_client.put_job_failure_result(jobId=event['CodePipeline.job']['id'],failureDetails={'type': 'JobFailed','message': 'Instance is not running','externalExecutionId': context.aws_request_id})
    

                
        
        
        
