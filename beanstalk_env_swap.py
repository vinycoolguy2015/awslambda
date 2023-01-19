import boto3
import os

def lambda_handler(event, context):
    client = boto3.client('elasticbeanstalk',region_name='us-west-1')
    codepipeline_client=boto3.client('codepipeline',region_name='us-west-1')
    #route53_client = boto3.client('route53')
    #lambda_client = boto3.client('lambda')
    try:
        client.swap_environment_cnames(SourceEnvironmentName='development-environment',DestinationEnvironmentName='production-environment')
        #prod_dns_name=os.environ['DEV_DNS_NAME']
        #dev_dns_name=os.environ['PROD_DNS_NAME']
        
        
        #lambda_client.update_function_configuration(FunctionName=os.environ['AWS_LAMBDA_FUNCTION_NAME'],Environment={'Variables': {'ALIAS_HOSTED_ZONE_ID': os.environ['ALIAS_HOSTED_ZONE_ID'],'YOUR_HOSTED_ZONE_ID': os.environ['YOUR_HOSTED_ZONE_ID'],'RECORD_NAME':os.environ['RECORD_NAME'],'DEV_DNS_NAME':dev_dns_name,'PROD_DNS_NAME':prod_dns_name}})
        codepipeline_client.put_job_success_result(jobId=event['CodePipeline.job']['id'])
    except Exception as e:
        print(e)
        codepipeline_client.put_job_failure_result(jobId=event['CodePipeline.job']['id'],failureDetails={'type': 'JobFailed','message': 'CNAME swapping failed','externalExecutionId': context.aws_request_id})
    


