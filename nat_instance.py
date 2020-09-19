import boto3
client = boto3.client('ec2')

NetworkInterfaceId='eni-xyz'
response = client.describe_route_tables()
subnetlist=[]
for routeTable in response['RouteTables']:
    for route in routeTable['Routes']:
        if 'NetworkInterfaceId' in route and route['NetworkInterfaceId']==NetworkInterfaceId:
            for subnets in  routeTable['Associations']:
                subnetlist.append(subnets['SubnetId'])
reservations=client.describe_instances()['Reservations']
for reservation in reservations:
   for instance in reservation['Instances']:
      if instance['SubnetId'] in subnetlist:
         for tag in instance['Tags']:
            if tag['Key']=='Name':
               print (instance['InstanceId'],tag['Value'])
