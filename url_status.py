from collections import defaultdict

import boto3
from botocore.vendored import requests

def write_metric(value, metric):

    d = boto3.client('cloudwatch')
    d.put_metric_data(Namespace='Website Status',
                      MetricData=[
                          {
                              'MetricName':metric,
                              'Dimensions':[
                                  {
                                      'Name': 'Status',
                                      'Value': 'WebsiteStatusCode',
                                  },
                              ],
                              'Value': value,
                          },
                      ]
                      )

def check_site(url, metric):

    STAT = 1
    print("Checking %s " % url)
    try:
        response = requests.head("http://" + url)
        response.close()
    except requests.exceptions.URLRequired as e:
        if hasattr(e, 'code'):
            print ("[Error:] Connection to %s failed with code: " %url +str(e.code))
            STAT = 100
            write_metric(STAT, metric)
        if hasattr(e, 'reason'):
            print ("[Error:] Connection to %s failed with code: " % url +str(e.reason))
            STAT = 100
            write_metric(STAT, metric)
    except requests.exceptions.HTTPError as e:
        if hasattr(e, 'code'):
            print ("[Error:] Connection to %s failed with code: " % url + str(e.code))
            STAT = 100
            write_metric(STAT, metric)
        if hasattr(e, 'reason'):
            print ("[Error:] Connection to %s failed with code: " % url + str(e.reason))
            STAT = 100
            write_metric(STAT, metric)
        print('HTTPError!!!')

    if STAT != 100:
        STAT = response.status_code
    print(STAT)

    return STAT
def lambda_handler(event, context):
    """
    A tool for retrieving basic information from the running EC2 instances.
    """
    
    # Connect to EC2
    ec2 = boto3.resource('ec2')
    ses = boto3.client('ses',region_name='us-east-1')
    
    # Get information for all running instances
    running_instances = ec2.instances.filter(Filters=[{
        'Name': 'instance-state-name',
        'Values': ['running']},{'Name':'tag:BILLING_ROLE','Values':[ 'Web']},{'Name':'tag:BILLING_ENVIRONMENT','Values':[ 'Integration']}])
    websiteurls=[]
    #ec2info = defaultdict()
    for instance in running_instances:
        # Add instance info to a dictionary         
	    websiteurls.append(instance.private_ip_address+":4503/crx/explorer/index.jsp")        
            
    print(websiteurls)    
    metricname = 'Site Availability'

    for site in websiteurls:
        r = check_site(site,metricname)
        if r == 200 or r == 403:
            print("Site %s is up" %site)
            write_metric(200, metricname)
        else:
            ses.send_email(Source='abc@abc.com',Destination={'ToAddresses': ["abc@abc.com"],'CcAddresses': ["abc@abc.com"]},
    
    Message={
        'Subject': {
            'Data': 'Server down Alert'
        },
        'Body': {
            'Text': {
                'Data': instance.private_ip_address+":4503/crx/explorer/index.jsp" ' is Down '
            }
        }
    }
)
            print("[Error:] Site %s down" %site)
            write_metric(50, metricname)
			
	
