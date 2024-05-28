import boto3
import requests
from requests_aws4auth import AWS4Auth
from datetime import datetime, timedelta

host = "https://<collection_id>.<region>.aoss.amazonaws.com/"
region = "us-east-1"
service = 'aoss'
threshold_days = 30
threshold_date = datetime.now() - timedelta(days=threshold_days)

credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
path = '_cat/indices?format=json&h=index,docs.count,health,store.size,status,creation.date.string'
url = host + path
payload = {}

headers = {"Content-Type": "application/json"}

response= requests.get(url, auth=awsauth, json=payload, headers=headers)

indices = response.json()
unused_indices = []
for index in indices:
    index_name = index['index']
    doc_count = int(index['docs.count'])
    
    # Fetch detailed stats for each index
    stats_response = requests.get(f'{host}/{index_name}', auth=awsauth)
    stats = stats_response.json()
    creation_date = datetime.fromtimestamp(int(stats[index_name]['settings']['index']['creation_date']) / 1000)
    # Check for recent activity
    is_unused = (doc_count == 0 or creation_date < threshold_date)
    if is_unused:
        unused_indices.append(index_name)

print("Unused indices:")
for idx in unused_indices:
    print(idx)
