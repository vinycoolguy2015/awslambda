import json
import os

import urllib3


def lambda_handler(event, context):
    alb1_url = '<ALB1_DNS>'
    alb2_url = '<ALB2_DNS>'

    # Two way to have http method following if lambda proxy is enabled or not
   
    if event.get('httpMethod'):
        http_method = event['httpMethod']
    else:
        http_method = event['requestContext']['http']['method']
    if event['path'] == '/alb1':
        url=alb1_url
    elif event['path'] == '/alb2':
        url=alb2_url
    headers = ''
    if event.get('headers'):
        headers = event['headers']
        # Important to remove the Host header before forwarding the request
        if headers.get('Host'):
            headers.pop('Host')
        if headers.get('host'):
            headers.pop('host')

    body = ''
    if event.get('body'):
        body = event['body']

    try:
        http = urllib3.PoolManager()
        resp = http.request(method=http_method, url=url,
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
