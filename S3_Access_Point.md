
With S3 Access Point, you can restrict access to folders inside S3 bucket, without creating multiple IAM users/roles with access to individual folder. Let's see how to setup this so that we can access S3 from EC2 instance:



**Step 1**: Create IAM role for EC2 instance with following policy. Here athena1989 is S3 bucket name. This policy allows this IAM role to read/write objects under folder1 and folder2

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::athena1989/folder1/*",
                "arn:aws:s3:::athena1989/folder1",
                "arn:aws:s3:::athena1989/folder2/*",
                "arn:aws:s3:::athena1989/folder2"
            ]
        }
    ]
}
```
**Step 2:** Now add a bucket policy like this to athena1989 bucket. Here 'tenant' is the role name we created in Step 1. This policy denies tenant role to access S3 bucket unless it is accessed via S3 access point.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Deny",
            "Principal": {
                "AWS": "arn:aws:iam::<AWS_ACCOUNT_ID>:role/tenant"
            },
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::athena1989",
                "arn:aws:s3:::athena1989/*"
            ],
            "Condition": {
                "StringNotLike": {
                    "s3:DataAccessPointArn": "arn:aws:s3:us-east-1:<AWS_ACCOUNT_ID>:accesspoint/*"
                }
            }
        }
    ]
}
```
**Step 3:** Now create S3 access point named folder1 of type VPC/Internet with public access blocked. Add following Access Point policy. This policy allow tenant role to read/write objects in folder1 folder of S3 bucket.

```
{
    "Version": "2008-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::<AWS_ACCOUNT_ID>:role/tenant"
            },
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:us-east-1:<AWS_ACCOUNT_ID>:accesspoint/folder1/object/folder1/*"
        }
    ]
}
```

**Step 4:** Repeat Step3 and create S3 access point named folder2 of type VPC/Internet with public access blocked. Add following Access Point policy. This policy allow tenant role to read/write objects in folder2 folder of S3 bucket.
```
{
    "Version": "2008-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::<AWS_ACCOUNT_ID>:role/tenant"
            },
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:us-east-1:<AWS_ACCOUNT_ID>:accesspoint/folder2/object/folder2/*"
        }
    ]
}
```

Step 5: We are done with the setup. You may launch an EC2 instance with tenant role attached to it and execute following commands to do some testing:

# Access Denied since tenant role is not allowed to access S3 bucket directly
aws s3 cp package.json s3://athena1989/folder1/
 
# Access Denied since tenant role is not allowed to access S3 bucket directly
aws s3 cp package.json s3://athena1989/folder2/
 
# Successful since tenant role has access to folder1 access point and that access point can read/write to folder1 folder
aws s3api put-object --body package.json --bucket arn:aws:s3:us-east-1:<AWS_ACCOUNT_ID>:accesspoint/folder1 --key folder1/package.json
 
# Access denied even though tenant role has access to folder1 access point but that access point can't read/write to folder2 folder
aws s3api put-object --body package.json --bucket arn:aws:s3:us-east-1:808658323399:accesspoint/folder1 --key folder2/package.json
 
# Successful since tenant role has access to folder2 access point and that access point can read/write to folder2 folder
aws s3api put-object --body package.json --bucket arn:aws:s3:us-east-1:<AWS_ACCOUNT_ID>:accesspoint/folder2 --key folder2/package.json 
 
# Access denied even though tenant role has access to folder2 access point but that access point can't read/write to folder1 folder
aws s3api put-object --body package.json --bucket arn:aws:s3:us-east-1:<AWS_ACCOUNT_ID>:accesspoint/folder2 --key folder1/package.json
