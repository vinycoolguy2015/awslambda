def lambda_handler(event, context):
    import boto3
    client = boto3.client('ec2')
    ami_list = event['Input']['Payload']['ami_list']
    target_filter=event['Input']['Payload']['target_filter']
    instance_list=event['Input']['Payload']['instance_list']
    for ami_id in ami_list:
        ami_created="False"
        response = client.describe_images(ImageIds=ami_list)
        for image_detail in response['Images']:
            if image_detail['State'] =='available':
                ami_created="True"
            else:
                break
                
    return{
        'ami_created': ami_created,
        'ami_list': ami_list,
        'target_filter': target_filter,
        'instance_list': instance_list
    }

