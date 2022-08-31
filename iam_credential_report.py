import boto3
import time
import csv
import os
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
