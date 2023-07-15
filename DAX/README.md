1-Create DAX Cluster with the Terraform code.
2-Launch an EC2 instance. Make sure the IAM role attached to it has following permisison.
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "dax:*"
            ],
            "Effect": "Allow",
            "Resource": [
                "<DAX_CLUSTER_ARN>"
            ]
        }
    ]
}
```
3-Connect to EC2 instance and execute following commands:

```
pip3 install amazon-dax-client
wget http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/samples/TryDax.zip
unzip TryDax.zip
```

4- Follow https://awstut.com/en/2022/12/29/accessing-dynamodb-accelerator-dax-with-ec2-lambda-en/ for testing.


Note-DAX maintains two caches for data that it reads from DynamoDB:

Item cache—For items retrieved using GetItem or BatchGetItem.
Query cache—For result sets retrieved using Query or Scan.

The default TTL for each of these caches is 5 minutes. If you want to use different TTL settings, you can launch a DAX cluster using a custom parameter group.

Reference: 
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.access-control.html
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.sizing-guide.html
https://github.com/devops-made-easy/terraform-aws-dax/tree/master
