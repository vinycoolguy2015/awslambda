import json
import sys
import pymysql
import boto3
import logging
import os
logger = logging.getLogger()
logger.setLevel(logging.INFO)
secretclient = boto3.client('secretsmanager')
# rds settings

ostype=os.environ['OS_TYPE']

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

def lambda_handler(event, context):

    database_secrets=get_db_creds()
    mydb=connect_db(database_secrets) 
    
    mycursor = mydb.cursor()
    sql = "select ImageId from test.ami where OperatingSystem='" + ostype + "' order by ImageDate desc limit 1;"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if not len(myresult) > 0:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "golden_ami_id": "No Records found"
        }
        
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "golden_ami_id": myresult[0][0]
    }
    
