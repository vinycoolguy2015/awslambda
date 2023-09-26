import urllib.request
import os
import json
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)

aws_session_token = os.environ.get('AWS_SESSION_TOKEN')

def lambda_handler(event, context):
    pipeline_id=event['pipeline_id']
    req = urllib.request.Request("http://localhost:2773//secretsmanager/get?secretId="+os.environ['SECRET_NAME'])
    req.add_header('X-Aws-Parameters-Secrets-Token', aws_session_token)
    config = urllib.request.urlopen(req).read()
    
    secret_data= json.loads(config)['SecretString']
    tokens=json.loads(secret_data)
    
    try:
       url=("https://gitlab.com/api/v4/projects/"+os.environ['GITLAB_PROJECT_ID']+"/pipelines/"+str(pipeline_id))
       hdr = { 'PRIVATE-TOKEN' :  tokens['PAT']}
       req = urllib.request.Request(url, headers=hdr)
       response = urllib.request.urlopen(req).read()
       return {
            "statusCode": 200,
            "headers": {
               "Content-Type": "application/json"
             },
            "pipeline_status": json.loads(response)['status'],
            "pipeline_id": pipeline_id
            }
    except Exception as e:
        logger.error("Pipeline status not available: " + str(e))
        return {
            "statusCode": 500,
            "headers": {
               "Content-Type": "application/json"
             },
            "pipeline_status": "",
            "pipeline_id": pipeline_id
            }
