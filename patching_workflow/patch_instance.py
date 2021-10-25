import boto3
import time
client = boto3.client('ssm')

def lambda_handler(event, context):
    target_filter=event['Input']['Payload']['target_filter']
    instance_list=event['Input']['Payload']['instance_list']
    response=client.send_command(
        Targets=[target_filter],
        DocumentName='AWS-RunPatchBaseline',
        DocumentVersion='$LATEST',
        TimeoutSeconds=900,
        Parameters={
              'Operation': [
                      'Install'
                        ],
                'RebootOption': [
                        'RebootIfNeeded'
                          ]
                },
        CloudWatchOutputConfig={
        'CloudWatchOutputEnabled': True
    }
        )
    commandId=response['Command']['CommandId']
    return {
        'commandId': commandId,
        'instance_list': instance_list
        }
    
