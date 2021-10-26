def lambda_handler(event, context):
    import boto3
    #import time
    ssm_client = boto3.client('ssm')
    ec2_client = boto3.client('ec2')
    instance_list=[]
    target_filter=event['Input']['Target']
    command=event['Input']['Command']
    
    # Scan for patches

    response=ssm_client.send_command(
        #InstanceIds=['i-0871c740183ca201e'],
        Targets=[target_filter],
        DocumentName='AWS-RunPatchBaseline',
        DocumentVersion='$LATEST',
        TimeoutSeconds=900,
        Parameters={
              'Operation': [
                      'Scan'
                        ],
                'RebootOption': [
                        'NoReboot'
                          ]
                },
        OutputS3BucketName='codepipeline-us-east-1-175848680181'
        )
    
    commandId=response['Command']['CommandId']
    
    #updated_target_filter=target_filter
    updated_target_filter=target_filter.copy()
    updated_target_filter['Name'] = updated_target_filter.pop('Key')
    
    response = ec2_client.describe_instances(Filters=[updated_target_filter])
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_list.append(instance['InstanceId'])
    return{
        'commandId': commandId,
        'instance_list': instance_list,
        'target_filter': target_filter,
        'command': command
    }
    
    
