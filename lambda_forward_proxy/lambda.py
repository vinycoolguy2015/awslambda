import json
import os

import urllib3
from urllib3 import ProxyManager

def lambda_handler(event, context):
    print(event)
    #url='https://<APIB_ID>-<VPCB_ENDPOINT_ID>.execute-api.<REGION>.amazonaws.com/<STAGE>'
    proxy_url='http://18.191.178.221:8888'

    # Two way to have http method following if lambda proxy is enabled or not
    if event.get('httpMethod'):
        http_method = event['httpMethod']
    else:
        http_method = event['requestContext']['http']['method']
    
    path=event.get('path')
    forward_domain=path.split('/',2)[1]
    forward_path=''
    if len(path.split('/')) > 2:
        forward_path=path.split('/',2)[2]
    
    
    if forward_domain=='api':
        forward_url='http://18.191.178.221:8080'
    
        
    
    
    #path=event.get('path')
    headers = ''
    queryStringParameters=''
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
    
    
    #headers['x-api-key']='eB44IFhHK31Tq4pBYVc5P7'

    body = ''
    if event.get('body'):
        body = event['body']
    if event.get('queryStringParameters'):
        queryStringParameters=event['queryStringParameters']
    

    try:
        #http = urllib3.PoolManager()
        http = ProxyManager(proxy_url)
        resp = http.request(method=http_method, url=forward_url+'/'+forward_path,headers=headers,fields=queryStringParameters,
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
