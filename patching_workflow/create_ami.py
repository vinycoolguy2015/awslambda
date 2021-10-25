def lambda_handler(event, context):
    import boto3
    from datetime import datetime
    import time

    client = boto3.client('ec2')
    ami_list=[]
    instance_list=event['Input']['Payload']['instance_list']
    target_filter=event['Input']['Payload']['target_filter']
    for instance in instance_list:
        response = client.describe_instances(InstanceIds=[instance])
        instance_name= [tag['Value'] for tag in response['Reservations'][0]['Instances'][0]['Tags'] if tag['Key'] == 'Name']
        response = client.create_image(
            InstanceId=instance,
            Name=instance_name[0]+"_"+datetime.now().strftime('%Y-%m-%d %H-%M-%S'),
            NoReboot=True,
            TagSpecifications=[
            {
                'ResourceType': 'image',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': instance_name[0]+"_"+datetime.now().strftime('%Y-%m-%d %H-%M-%S')
                    },
                ]
            },
        ])
        ami_list.append(response['ImageId'])
        time.sleep(10)
    return {
        'ami_list':ami_list,
        'target_filter': target_filter,
        'instance_list': instance_list
        
    }
    
   
