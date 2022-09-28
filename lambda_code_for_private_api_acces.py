import json
import os

import urllib3


def lambda_handler(event, context):
    #url='https://<API_ID>-<VPC_ENDPOINT_ID>.execute-api.<REGION>.amazonaws.com/<STAGE_NAME>'
    url='https://tc1wd0zoqk-vpce-03792931afc159093.execute-api.us-east-2.amazonaws.com/test'

    # Two way to have http method following if lambda proxy is enabled or not
    if event.get('httpMethod'):
        http_method = event['httpMethod']
    else:
        http_method = event['requestContext']['http']['method']

    headers = ''
    if event.get('headers'):
        headers = event['headers']

    # Important to remove the Host header before forwarding the request
    if headers.get('Host'):
        headers.pop('Host')

    if headers.get('host'):
        headers.pop('host')
    
    if headers.get('x-amzn-vpc-id'):
        headers.pop('x-amzn-vpc-id')
    
    if headers.get('x-amzn-vpce-config'):
        headers.pop('x-amzn-vpce-config')
    
    if headers.get('x-amzn-vpce-id'):
        headers.pop('x-amzn-vpce-id')
    headers['x-api-key']='xyz'

    body = ''
    if event.get('body'):
        body = event['body']

    try:
        http = urllib3.PoolManager()
        resp = http.request(method=http_method, url=url, headers=headers,
                            body=body)

        body = {
            "result": resp.data.decode('utf-8')
        }

        response = {
            "statusCode": resp.status,
            "body": json.dumps(body)
        }
    except urllib3.exceptions.NewConnectionError:
        print('Connection failed.')
        response = {
            "statusCode": 500,
            "body": 'Connection failed.'
        }

    return response
