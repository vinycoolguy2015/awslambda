import psycopg2
import random
import string
import time
import botocore 
import botocore.session 
from aws_secretsmanager_caching import SecretCache, SecretCacheConfig 
from psycopg2 import OperationalError, InterfaceError, DatabaseError
import json

#Fetch credentials from Secret Manager
client = botocore.session.get_session().create_client('secretsmanager')
cache_config = SecretCacheConfig(secret_refresh_interval=30)
cache = SecretCache( config = cache_config, client = client)

#Establishing the connection
while True:
    print("------------------")
    time.sleep(1)
    try:
        secret =json.loads( cache.get_secret_string('<SECRET_NAME>'))
        conn = psycopg2.connect(database="mylab", user=secret['username'], password=secret['password'], host='<DATABASE_WRITER_ENDPOINT>', port= '5432',connect_timeout=3)
        conn.autocommit = True

        cursor = conn.cursor()
        letters = string.ascii_letters
        name=''.join(random.choice(letters) for i in range(50)) 

        cursor.execute("INSERT INTO accounts(EMPLOYEE) VALUES (%s);", (name,))
        conn.commit()
        print("Records inserted "+name)
    except (OperationalError, InterfaceError, DatabaseError) as e:
         print(f"Database connection error: {e}")
    except Exception as e:
        print("Error writing data")
        print(e)
    try:
        secret =json.loads( cache.get_secret_string('<SECRET_NAME>'))
        conn1 = psycopg2.connect(database="mylab", user=secret['username'], password=secret['password'], host='<DATABASE_WRITER_ENDPOINT>', port= '5432',connect_timeout=3)
        cursor = conn1.cursor()
        cursor.execute("SELECT count(*) from accounts;")
        result = cursor.fetchone()
        print("Table count is "+str(result[0]))
    except (OperationalError, InterfaceError, DatabaseError) as e:
         print(f"Database connection error: {e}")
    except Exception as e:
        print("Error reading data")
        print(e)
