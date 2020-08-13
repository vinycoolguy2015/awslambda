import pymysql
import logging
import sys
import json

def lambda_handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    try:
        conn = pymysql.connect("datbase_host", user="admin", passwd="password", db="rds", connect_timeout=5)
    except pymysql.MySQLError as e:
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(e)
        sys.exit()

    logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")

    with conn.cursor() as cur:
        query_statement = "show processlist"
        cur.execute(query_statement)
        result = cur.fetchall()
        logger.info("Result: " + json.dumps(result, indent=2))
