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


access_keys=[]

for access_key in access_keys:
    try:
        response = account1_client.get_access_key_last_used(AccessKeyId=access_key)
    except ClientError as e:
        try:
            response = account2_client.get_access_key_last_used(AccessKeyId=access_key)
        except ClientError as e:
            print("Access key %s not found in the given AWS accounts." % (access_key))
        else:
            print( "Access_key %s found in account2"% (access_key))
    else:
        print( "Access_key %s found in account1"% (access_key))
