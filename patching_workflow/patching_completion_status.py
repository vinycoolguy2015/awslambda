def lambda_handler(event, context):
    import boto3
    import os 
    sns_client = boto3.client("sns")
    ssm_client= boto3.client('ssm')
    ec2_client= boto3.client('ec2')
    message=[]
    instance_list=event['Input']['Payload']['instance_list']
    
    for instance in instance_list:
        response = ec2_client.describe_instances(InstanceIds=[instance])
        instance_name= [tag['Value'] for tag in response['Reservations'][0]['Instances'][0]['Tags'] if tag['Key'] == 'Name']
        #response = ssm_client.list_compliance_items(ResourceIds=[instance],ResourceTypes=['ManagedInstance'])
        #print(response['ComplianceItems'][0]['Status'])
        response=ssm_client.describe_instance_patch_states(InstanceIds=[instance])
        #if response['ComplianceItems'][0]['Status'] == 'COMPLIANT':
        if response['InstancePatchStates'][0]['MissingCount'] > 0:
            message.append(instance_name[0]+"("+instance+") not patched.\n")
        else:
            message.append(instance_name[0]+"("+instance+") patched.\n")
        
    
    sns_client.publish(TopicArn=os.environ['SNS_TOPIC'], Message=''.join(message) ,Subject="Patching Status")
