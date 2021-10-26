import time
import boto3

def lambda_handler(event, context):
    ssm_client = boto3.client('ssm')
    instance_list=event['Input']['Payload']['instance_list']
    target_filter=event['Input']['Payload']['target_filter']
    command=event['Input']['Payload']['command']
    response = ssm_client.send_command(Targets=[target_filter],DocumentName="AWS-RunShellScript",Parameters={'commands': [command]} )
    command_id = response['Command']['CommandId']
    return {
    'instance_list': instance_list,
    'target_filter': target_filter,
    'command_id': command_id
        }
