import boto3

def lambda_handler(event, context):
    client = boto3.client('imagebuilder')
    image_builder_arn=event['image_builder_arn']
    while True:
        response = client.get_image(imageBuildVersionArn=image_builder_arn)
        image_status=response['image']['state']['status']
        if image_status == 'AVAILABLE':
            return {'image_builder_arn':image_builder_arn, 'status':'application ami available','application_ami_id':response['image']['outputResources']['amis'][0]['image']}
            break
        else:
            return {'image_builder_arn':image_builder_arn,'status': 'application ami still not available'}
 
