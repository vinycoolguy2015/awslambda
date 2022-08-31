import os
import boto3
import time
import csv
import pandas as pd
client = boto3.client('iam')
completion_status=""
response = client.generate_credential_report()
while completion_status != "COMPLETE":
    time.sleep(5)
    completion_status=response['State']
response = client.get_credential_report()
with open("creds.csv", 'w') as csvFile:
    lns = response['Content'].split("\n")
    for item in lns:
        csvFile.write(item.replace("=", ",") + os.linesep)
data=pd.read_csv("creds.csv", usecols=['user', 'access_key_1_last_rotated', 'access_key_2_last_rotated'])
print(data)
