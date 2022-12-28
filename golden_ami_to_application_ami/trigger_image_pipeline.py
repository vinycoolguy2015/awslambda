import boto3
import os

def lambda_handler(event, context):
    client = boto3.client('imagebuilder')
    cfclient = boto3.client('cloudformation')

    stack_detail = cfclient.describe_stacks(StackName=os.environ['STACK_NAME'])
    image_pipeline_arn=stack_detail['Stacks'][0]['Outputs'][0]['OutputValue'] # This needs to be changed

    response = client.start_image_pipeline_execution(imagePipelineArn=image_pipeline_arn)
    return {'image_builder_arn' : response['imageBuildVersionArn']}
