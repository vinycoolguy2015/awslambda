import json
import sys
import pymysql
import boto3
import logging
import os
from datetime import date

logger = logging.getLogger()
logger.setLevel(logging.INFO)
secretclient = boto3.client('secretsmanager')


ostype=os.environ['OS_TYPE']
todays_date = date.today()
ami_date='-'.join([str(todays_date.year),str(todays_date.month),str(todays_date.day)])

def get_db_creds():
    secret_id = os.environ['SECRET_NAME']
    response = secretclient.get_secret_value(SecretId=secret_id)
    db_creds= json.loads(response['SecretString'])
    return db_creds

def connect_db(database_secrets):
    try:
        connection = pymysql.connect( user=database_secrets['username'], password=database_secrets['password'], database=database_secrets['dbname'], host=database_secrets['host'], port=int(database_secrets['port']), connect_timeout=5)
        logger.info("SUCCESS: Connection to RDS Aurora instance succeeded")
        return connection
    except pymysql.MySQLError as e:
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(e)
        fail_error= str(e)
        sys.exit()
        
def put_into_db(connection,image_id):
    try:
        Region = 'us-east-1'
        OperatingSystem =ostype
        
        ImageDate =ami_date
        with connection.cursor() as cur:
            cur.execute('insert into application_ami (Region, OperatingSystem, ImageId, ImageDate) values("'+Region+'","'+OperatingSystem+'","'+image_id+'","'+ImageDate+'")')
        connection.commit()
        cur.close()
        logger.info ("SUCCESS : All application AMI data has been inserted into Aurora DB")
    except Exception as e:
        logger.error("Execution failed: " + str(e))
        connection.rollback()
        logger.error("Failed to commit changes in the DB, do rollback")
        fail_error= str(e)
        

def lambda_handler(event, context):
    
    try:
        database_secrets=get_db_creds()
        connection=connect_db(database_secrets) 
        put_into_db(connection,event['application_ami_id'])
        connection.close()
    except Exception as e:
        logger.error("Execution failed: " + str(e))
        fail_error= str(e)
    
    
       
