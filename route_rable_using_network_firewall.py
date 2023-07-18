import boto3
vpc_mapping = {
  "vpc-zxzxzxx":"dev",
  "vpc-sfsdfdsf":"sit",
  "vpc-sdvdsf":"stg",
  "vpc-dsvdsfg":"uat"
}

def get_gateway_load_balancer_endpoints():
    # Replace 'your_region' with the AWS region where your VPC endpoints are located
    region = 'ap-southeast-1'

    # Create a Boto3 EC2 client
    ec2_client = boto3.client('ec2', region_name=region)

    # Describe all VPC endpoints in the region
    response = ec2_client.describe_vpc_endpoints()

    # Filter VPC endpoints with type 'GatewayLoadBalancer'
    gateway_lb_endpoints = []
    for endpoint in response['VpcEndpoints']:
        if endpoint['VpcEndpointType'] == 'GatewayLoadBalancer':
            gateway_lb_endpoints.append(endpoint)

    return gateway_lb_endpoints

def get_route_tables_by_target(target_id):
    # Replace 'your_region' with the AWS region where your route tables are located
    region = 'ap-southeast-1'

    # Create a Boto3 EC2 client
    ec2_client = boto3.client('ec2', region_name=region)

    # Describe all route tables in the region
    response = ec2_client.describe_route_tables()

    # Filter route tables with the specified target
    route_tables_with_target = []
    for route_table in response['RouteTables']:
        for route in route_table['Routes']:
            if 'GatewayId' in route and route['GatewayId'] == target_id:
                route_tables_with_target.append(route_table['RouteTableId'])

    return route_tables_with_target

# Get VPC endpoints of type 'GatewayLoadBalancer'
gateway_lb_endpoints = get_gateway_load_balancer_endpoints()

if gateway_lb_endpoints:
    print("GatewayLoadBalancer endpoints:")
    for endpoint in gateway_lb_endpoints:
        print(f"VPC Endpoint ID: {endpoint['VpcEndpointId']}")
        print(f"VPC ID: {endpoint['VpcId']}")
        vpc_name=vpc_mapping.get(endpoint['VpcId'], 'Key not found')
        print(f"VPC Name: {vpc_name}")
        route_tables = get_route_tables_by_target(endpoint['VpcEndpointId'])
        rt_list=[]
        if route_tables:
            print("Route tables with the specified target:")
            for rt_id in route_tables:
                if rt_id not in rt_list:
                    rt_list.append(rt_id)
            print(rt_list)
        else:
            print("No route tables found with the specified target.")
        print("---")

else:
    print("No GatewayLoadBalancer endpoints found.")
