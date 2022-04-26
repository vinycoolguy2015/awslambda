import boto3
import json
client = boto3.client('ssm')


def lambda_handler(event, context):
    try:
        if event['queryStringParameters'] is not None:
            parameter_name=event['queryStringParameters']['name']
            response = client.get_parameter(Name= parameter_name,WithDecryption=True)
            parameter_value=response['Parameter']['Value']
            return {'statusCode': 200,'body': json.dumps(parameter_value)}
        
        else:
            params=[]
            p = client.get_paginator('describe_parameters')
            paginator = p.paginate().build_full_result()
            for page in paginator['Parameters']:
                params.append(page['Name'])
            return {'statusCode': 200,'body': json.dumps(params)}
    except Exception as e:
        print(e)
        return {'statusCode': 500,'body': json.dumps("Error fetching parameter value.May be parameter name is incorrect or you do not have permission to access it.")}
        


