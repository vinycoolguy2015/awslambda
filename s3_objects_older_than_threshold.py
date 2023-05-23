import boto3
from datetime import datetime, timedelta
from pytz import timezone

# Specify your bucket name
bucket_name = "<bucket_name>"

# Create an S3 client
s3 = boto3.client("s3",region_name='us-east-1')

# Calculate the time threshold
current_time = datetime.utcnow()
threshold_time = current_time - timedelta(minutes=30)

# Retrieve S3 objects
response = s3.list_objects_v2(Bucket=bucket_name)

# Iterate over the objects and filter by last modified time
if "Contents" in response:
    for obj in response["Contents"]:
        last_modified = obj["LastModified"].replace(tzinfo=None)
        # Check if last modified time is greater than threshold
        if last_modified < threshold_time:
            object_key = obj["Key"]
            print("Object key:", object_key,last_modified,threshold_time)
            
        else:
            print("New objects")
            print("Object key:", object_key,last_modified,threshold_time)
else:
    print("No objects found in the bucket.")
