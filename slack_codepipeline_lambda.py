import json
import logging
import os
import urllib3

http = urllib3.PoolManager()
# Read environment variables
SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']
SLACK_CHANNEL = os.environ['SLACK_CHANNEL']
SLACK_USER = os.environ['SLACK_USER']
logger = logging.getLogger()
logger.setLevel(logging.INFO)
def lambda_handler(event, context):
    logger.info("Event: " + str(event))
    
# Construct a slack message
    slack_message = {
        'channel': SLACK_CHANNEL,
        'username': SLACK_USER,
        'text': event['detail']['pipeline']+" pipeline execution "+event['detail']['state']
    }
# Post message on SLACK_WEBHOOK_URL
    r = http.request('POST', SLACK_WEBHOOK_URL,body=json.dumps(slack_message))
