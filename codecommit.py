import boto3

def lambda_handler(event, context):
    repo='test'
    normal_sns='arn:aws:sns:us-east-1:953898941182:normal'
    emergency_sns='arn:aws:sns:us-east-1:953898941182:emergency'
    codecommit_client = boto3.client('codecommit')
    sns_client = boto3.client('sns')
    commitresponse = codecommit_client.get_differences(repositoryName=repo,afterCommitSpecifier=event['Records'][0]['codecommit']['references'][0]['commit'])
    for differences in commitresponse['differences']:
        if differences['afterBlob']['path'] == 'normal.txt':
            data = codecommit_client.get_file(repositoryName=repo,filePath=differences['afterBlob']['path'])
            endpoint=data['fileContent'].decode("utf-8").strip()
            sns_client.subscribe(TopicArn=normal_sns,Protocol='email',Endpoint=endpoint)
        elif differences['afterBlob']['path'] == 'critical.txt':
            data = codecommit_client.get_file(repositoryName=repo,filePath=differences['afterBlob']['path'])
            endpoint=data['fileContent'].decode("utf-8").strip()
            sns_client.subscribe(TopicArn=emergency_sns,Protocol=email,Endpoint=endpoint)
