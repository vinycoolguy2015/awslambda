import os
from datetime import datetime, timedelta
import boto3
import time
import csv
import pandas as pd

rotation_threshold=90

client = boto3.client('iam')
response = client.generate_credential_report()
completion_status=response['State']
while completion_status != "COMPLETE":
    time.sleep(5)
    response = client.generate_credential_report()
    completion_status=response['State']
response = client.get_credential_report()
with open("creds.csv", 'w') as csvFile:
    lns = response['Content'].split("\n")
    for item in lns:
        csvFile.write(item.replace("=", ",") + os.linesep)

data=pd.read_csv("creds.csv", usecols=['user', 'access_key_1_last_rotated', 'access_key_2_last_rotated'])

for i, record in data.iterrows():
    record['access_key_1_last_rotated'] = pd.to_datetime(record['access_key_1_last_rotated'])
    record['access_key_2_last_rotated'] = pd.to_datetime(record['access_key_2_last_rotated'])
    time_between_access_key1_rotation = datetime.utcnow().date() - datetime.date(record['access_key_1_last_rotated'])
    time_between_access_key2_rotation = datetime.utcnow().date() - datetime.date(record['access_key_2_last_rotated'])
    if (time_between_access_key1_rotation > timedelta(days = rotation_threshold) or time_between_access_key2_rotation > timedelta(days = rotation_threshold)) and 'root' not in record['user']:
        print("Time to rotate access key for "+record['user'])
