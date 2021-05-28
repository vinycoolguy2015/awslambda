def lambda_handler(event, context):
    from botocore.vendored import requests
    import boto3
    ec2 = boto3.client('ec2')  
    print(requests.get('http://ip.42.pl/raw').text)
    ec2.stop_instances(InstanceIds=['i-033aa1badea1496b6']) #Specify NAT instance id
