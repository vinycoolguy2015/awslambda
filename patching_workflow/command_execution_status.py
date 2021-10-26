def lambda_handler(event, context):
    import boto3
    client = boto3.client('ssm')
    instance_list=event['Input']['Payload']['instance_list']
    target_filter=event['Input']['Payload']['target_filter']
    command_id=event['Input']['Payload']['command_id']
    for instance in instance_list:
        command_executed="False"
        response = client.get_command_invocation(CommandId=command_id,InstanceId=instance)
        command_execution_status = response['Status']
        if command_execution_status == "Success":
            command_executed="True"
        elif command_execution_status == "Failed":
            command_executed="Failed"
        else:
            break
            
       
            
        
    return{
        'command_executed': command_executed,
        'instance_list': instance_list,
        'command_id': command_id,
        'target_filter': target_filter
    }
