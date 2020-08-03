import boto3

def lambda_handler(event, context):
    client = boto3.client('codecommit')
    commitresponse = client.get_differences(repositoryName='test',afterPath='/master',afterCommitSpecifier=event['Records'][0]['codecommit']['references'][0]['commit'])
    for differences in commitresponse['differences']:
        if differences['afterBlob']['path'] == 'b.txt':
            data = client.get_file(repositoryName='test',filePath='master/'+differences['afterBlob']['path'])
            print(data['fileContent'])
