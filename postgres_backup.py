import subprocess
import argparse
import sys
import boto3

parser = argparse.ArgumentParser(description='Dump a PostGres databse to S3 or local')
parser.add_argument('url', help='postgres URL to connect to')
parser.add_argument('driver', choices=['s3', 'local'], default='local')
parser.add_argument('location', help='S3 bucket name or local path')


args = parser.parse_args()
if args.driver == 'local':
  try:
    command="pg_dump "+args.url+" >"+args.location
    subprocess.Popen(command,shell=True)
  except Exception as e:
    print(e)
    sys.exit(1)
elif args.driver == 's3':
  try:
    command="pg_dump "+args.url+" >/tmp/backup.txt"
    subprocess.Popen(command,shell=True)
    s3 = boto3.client('s3')
    with open('/tmp/backup.sql', 'rb') as data:
        s3.upload_fileobj(data, 'bucket', 'data_backup.sql')
  except Exception as e:
    print(e)
    sys.exit(1)
