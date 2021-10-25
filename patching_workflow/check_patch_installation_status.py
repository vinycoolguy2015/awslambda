def lambda_handler(event, context):
    import boto3
    client = boto3.client('ssm')
    instance_list=event['Input']['Payload']['instance_list']
    command_id=event['Input']['Payload']['commandId']
    for instance in instance_list:
        patch_installed="False"
        response = client.get_command_invocation(CommandId=command_id,InstanceId=instance)
        command_execution_status = response['Status']
        if command_execution_status == "Success":
            patch_installed="True"
        elif command_execution_status == "Failed":
            patch_installed="Failed"
        else:
            break
            
        
    return{
        'patch_installation_status': patch_installed,
        'instance_list': instance_list,
        'commandId': command_id
    }
