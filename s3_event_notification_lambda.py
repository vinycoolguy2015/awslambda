import boto3 
import botocore
from urllib.parse import unquote_plus
import json
import os
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.resource('s3')

def lambda_handler(event, context):
    print(event)
        
    key = unquote_plus(event['Records'][0]['s3']['object']['key'])
    event_name = event['Records'][0]['eventName']  
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    destination_bucket = os.environ['destination_bucket']
    
    source = {'Bucket': source_bucket, 'Key': key}
        
    if event_name == 'ObjectCreated:Put':
        try:
            response = s3.meta.client.copy(source, destination_bucket, key)
            logger.info("File copied to the destination bucket successfully.File name is "+key)
        
        except botocore.exceptions.ClientError as error:
            logger.error("There was an error copying the file to the destination bucket.File name is "+key)
            print('Error Message: {}'.format(error))
        
        except botocore.exceptions.ParamValidationError as error:
            logger.error("Missing required parameters while calling the API.")
            print('Error Message: {}'.format(error))
    elif event_name == 'ObjectRemoved:Delete':
        try:
            response = s3.Object(destination_bucket, key).delete()
            logger.info("File deleted from the destination bucket successfully.File name is "+key)
        
        except botocore.exceptions.ClientError as error:
            logger.error("There was an error deleting the file in the destination bucket.File name is "+key)
            print('Error Message: {}'.format(error))
        
        except botocore.exceptions.ParamValidationError as error:
            logger.error("Missing required parameters while calling the API.")
            print('Error Message: {}'.format(error))
    else:
        logger.info("Event not processed "+event)
        
