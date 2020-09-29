def lambda_handler(event, context):
    import boto3
    client = boto3.client('ec2')
    response = client.associate_iam_instance_profile(
    IamInstanceProfile={
        'Arn': '',
        'Name': ''
    },
    InstanceId=event['Input']['Payload']
    )
