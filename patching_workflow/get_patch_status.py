def lambda_handler(event, context):
    import boto3
    client = boto3.client('ssm')
    instance_list=event['Input']['Payload']['instance_list']
    target_filter=event['Input']['Payload']['target_filter']
    command=event['Input']['Payload']['command']
    response = client.describe_instance_patch_states(InstanceIds=instance_list)

    #Get Patch details
    for instance_id in instance_list:
        response = client.describe_instance_patches(InstanceId=instance_id,MaxResults=50,Filters=[
            {
                'Key': 'State',
                'Values': [
                    'Missing'
                ]
            },
        ])
        results = response["Patches"]
        while "NextToken" in response:
            response = client.describe_instance_patches(InstanceId=instance_id,MaxResults=50,NextToken=response['NextToken'],Filters=[
            {
                'Key': 'State',
                'Values': [
                    'Missing'
                ]
            },
        ])
        results.extend(response["Patches"])
        print("Package status on "+ instance_id+" before patching\n"+str(results))
        
    return{
    'instance_list': instance_list,
    'target_filter': target_filter,
    'command': command
        }
