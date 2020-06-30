import boto3
import csv
import os
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta


def send_report(subject,from_email,to_email,attachment):
    client = boto3.client('ses')
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    msg.preamble = 'Network Report\n'
    part = MIMEText('Hi,\n\nPFA Network report.\n\nNote: This is a system generated email do not reply.')
    msg.attach(part)
    part = MIMEApplication(open(attachment, 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename=attachment.split('/')[-1])
    msg.attach(part)
    result = client.send_raw_email(
        RawMessage={'Data': msg.as_string()},
        Source=msg['From'],
        Destinations=[msg['To']])

def lambda_handler(event, context):
    regions=['us-east-1','eu-west-1','ap-northeast-1']
    output_file='/tmp/network_details.csv'
    csv_file = open(output_file,'w+')
    csv_file.write("Region,VPCId,VPCCidr,VPCName,SubnetId,SubnetCidr,SubnetAZ,SubnetName,AvailableIPs,RouteTableId,RouteTableName,GatewayId,NACLId,InstanceCount,Instances\n\n")
    for region in regions:
        client = boto3.client('ec2',region_name=region)
        vpc_list = client.describe_vpcs(Filters=[{'Name': 'isDefault','Values': ['false']}])
        for vpc in vpc_list['Vpcs']:
            vpcid=vpc['VpcId']
            vpccidr=vpc['CidrBlock']
            if 'Tags' in vpc:
                for tags in vpc['Tags']:
                    if tags["Key"] == 'Name':
                        vpcname = tags["Value"]
            subnets = client.describe_subnets(Filters=[{'Name': 'vpc-id','Values': [vpcid]}])
        
            for subnet in subnets['Subnets']:
                subnetcidr=subnet['CidrBlock']
                subnetid=subnet['SubnetId']
                subnetaz=subnet['AvailabilityZone']
                availableip=subnet['AvailableIpAddressCount']
                gateway_id=''
                routetablename=''
                instancecount=0
                instances=[]
                if 'Tags' in subnet:
                    for tags in subnet['Tags']:
                        if tags["Key"] == 'Name':
                            subnetname = tags["Value"]
                route_table_data=client.describe_route_tables(Filters=[{'Name': 'association.subnet-id','Values': [subnetid]}])
                nacl= client.describe_network_acls(Filters=[{'Name': 'association.subnet-id','Values': [subnetid]}])
                naclid=nacl['NetworkAcls'][0]['NetworkAclId']
                routetableid=route_table_data['RouteTables'][0]['RouteTableId']
                if 'Tags' in route_table_data['RouteTables'][0]:
                    for tags in route_table_data['RouteTables'][0]['Tags']:
                        if tags["Key"] == 'Name':
                            routetablename = tags["Value"]
                for route in route_table_data['RouteTables'][0]['Routes']:
                    if 'DestinationCidrBlock' in route:
                        if route['DestinationCidrBlock']=='0.0.0.0/0':
                            if 'GatewayId' in route:
                                gateway_id=route['GatewayId']
                            elif 'InstanceId' in route:
                                gateway_id=route['InstanceId']
                            elif 'NatGatewayId' in route:
                                gateway_id=route['NatGatewayId']
                instancedata = client.describe_instances(Filters=[{'Name': 'subnet-id','Values': [subnetid]}])
                for reservation in instancedata['Reservations']:
                    if len(reservation['Instances']) >0:
                        for instance in reservation['Instances']:
                            instancename="Unnamed Instance"
                            if 'Tags' in instance:
                                for tags in instance['Tags']:
                                    if tags["Key"] == 'Name':
                                        instancename = tags["Value"]
                                        instances.append(instancename)
            
               
            
                csv_file.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(region,vpcid,vpccidr,vpcname,subnetid,subnetcidr,subnetaz,subnetname,availableip,routetableid,routetablename,gateway_id,naclid,len(instances),':::'.join(instances)))
            csv_file.flush()
    send_report("Network Report",os.environ['sender'],os.environ['receiver'],output_file)
        
    
