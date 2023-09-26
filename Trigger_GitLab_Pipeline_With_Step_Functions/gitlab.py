import urllib.request
import os
import json
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)

aws_session_token = os.environ.get('AWS_SESSION_TOKEN')

def lambda_handler(event, context):
    req = urllib.request.Request("http://localhost:2773//secretsmanager/get?secretId="+os.environ['SECRET_NAME'])
    req.add_header('X-Aws-Parameters-Secrets-Token', aws_session_token)
    config = urllib.request.urlopen(req).read()
    
    secret_data= json.loads(config)['SecretString']
    tokens=json.loads(secret_data)
    
    try:
       req = urllib.request.Request("https://gitlab.com/api/v4/projects/"+os.environ['GITLAB_PROJECT_ID']+"/ref/main/trigger/pipeline?token="+tokens['TRIGGER_TOKEN'],method="POST")
       config = urllib.request.urlopen(req).read()
       pipeline_data=json.loads(config)
       if 'id' in pipeline_data:
          logger.info("Pipeline Created")
          return {
            "statusCode": 200,
            "headers": {
               "Content-Type": "application/json"
             },
            "pipeline_id": pipeline_data['id']
            }
       else:
          return {
             "statusCode": 500,
              "headers": {
                  "Content-Type": "application/json"
                },
               "pipeline_id": ""
            }
    except Exception as e:
        logger.error("Pipeline Execution failed: " + str(e))
        return {
            "statusCode": 500,
            "headers": {
               "Content-Type": "application/json"
             },
            "pipeline_id": ""
            }
