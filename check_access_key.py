import os,re
import boto3
from botocore.exceptions import ClientError

account1_client = boto3.client(	'iam',
			aws_access_key_id="",
			aws_secret_access_key=""
		)
account2_client = boto3.client(   'iam',
                        aws_access_key_id="",
                        aws_secret_access_key=""
                ) 

rootDir= ""
access_keys=[]

for dirName, subdirList, fileList in os.walk(rootDir):
	for fname in fileList:
		if fname == 'api.json':
			filename=os.path.join(dirName, fname)
			text = open(filename, "r")
			for line in text.readlines():
				if re.search("accessKey", line):
					access_key=line.split(": ")[-1].rstrip()[1:-2]
					if access_key not in access_keys:
						access_keys.append(access_key)
						try:
							response = account1_client.get_access_key_last_used(AccessKeyId=access_key)
						except ClientError as e:
							try:
								response = account2_client.get_access_key_last_used(AccessKeyId=access_key)
							except ClientError as e:
								print("Access key %s used in %s not found in account1 or account2 account." % (access_key,dirName))
							else:
								print( "Access_key %s used in %s found in account2 account"% (access_key,dirName))
						else:
							print( "Access_key %s used in %s found in account1 account"% (access_key,dirName))
			
