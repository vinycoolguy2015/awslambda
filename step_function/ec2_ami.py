def lambda_handler(event, context):
    import boto3
    ec2= boto3.client('ec2')
    response=ec2.create_image( InstanceId=event['Input']['detail']['instance-id'],Name=event['Input']['detail']['instance-id'],NoReboot=True)
    return(event['Input']['detail']['instance-id'])
