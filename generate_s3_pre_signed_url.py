import boto3 

s3 = boto3.resource( 's3', aws_access_key_id='AKIA3YR6KY7',  aws_secret_access_key='tOyXzHmMSD4yARQpr)  

s3_client = boto3.client( 's3', aws_access_key_id='AKIA3YR6KY7',  aws_secret_access_key='tOyXzHmMSD4yARQpr) 

#Then use the session to get the resource 
my_bucket = s3.Bucket('config-bucket-2022') 
l=[]
for my_bucket_object in my_bucket.objects.all():
    object_key=my_bucket_object.key 
    l.append(object_key)
for i in l:
    url = s3_client.generate_presigned_url( ClientMethod='get_object', Params={'Bucket': 'config-bucket-2022', 'Key': i}, ExpiresIn=60)
    print(url)
