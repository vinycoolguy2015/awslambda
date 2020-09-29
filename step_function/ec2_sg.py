def lambda_handler(event, context):
    import boto3
    client = boto3.client('ec2')
    response = client.modify_instance_attribute(InstanceId=event['Input']['Payload'],Groups=['sg-xyz'])
