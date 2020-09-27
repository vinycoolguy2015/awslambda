import boto3
import os

def send_email(subject,body):
    ses_client=boto3.client("ses")
    ses_client.send_email(Source=os.environ['Source'],Destination={'ToAddresses': ['abc@xyz.com','def@xyz.com']},
    Message={
        'Subject': {
            'Data': subject
        },
        'Body': {
            'Text': {
                'Data': body
            }
        }
    }
)

def lambda_handler(event, context):
    instance_count={
        "us-east-1":{'Services':4,'NNA Publisher':3,'Publisher':4,'NNA Publisher Backup':1,'Publisher Backup':1},
        "eu-west-1":{'Services':2,'Publisher':6,'Publisher Backup':1},
        "ap-northeast-1":{'Services':2,'Publisher':6,'Publisher Backup':1}
    }
    
    notifications=[]
    
    
    regions=['us-east-1','ap-northeast-1','eu-west-1']
    
    
    for region in regions:
        client = boto3.client('ec2',region_name=region)
        if region == 'us-east-1':
            nna_publisher_instances= client.describe_instances(
            Filters=[
                {'Name': 'tag:BILLING_ENVIRONMENT','Values': ['PRODUCTION-nna']},
                {'Name': 'tag:BILLING_ROLE','Values': ['Publisher']},
                {'Name': 'instance-state-name','Values':['running']}
                ])
            nna_publisher_instances_count=0
            backup_nna_publisher_instances_count=0
            for reservation in nna_publisher_instances['Reservations']:
                for instance in reservation['Instances']:
                    for tags in instance['Tags']:
                        if tags["Key"] == 'Name' and 'backup' in tags["Value"]:
                            backup_nna_publisher_instances_count=backup_nna_publisher_instances_count+1
                            break
                        elif tags["Key"] == 'Name' and 'backup' not in tags["Value"]:
                            nna_publisher_instances_count=nna_publisher_instances_count+1
                            break
            if nna_publisher_instances_count != instance_count[region]['NNA Publisher']:
                Data=str(nna_publisher_instances_count)+ ' NNA Publishers running instead of '+str(instance_count[region]['NNA Publisher'])
                notifications.append(Data)
            
            if backup_nna_publisher_instances_count != instance_count[region]['NNA Publisher Backup']:
                Data=str(backup_nna_publisher_instances_count)+ ' NNA Backup Publishers running instead of '+str(instance_count[region]['NNA Publisher Backup'])
                notifications.append(Data)
		
            
        publisher_instances= client.describe_instances(
            Filters=[
                {'Name': 'tag:BILLING_ENVIRONMENT','Values': ['PRODUCTION']},
                {'Name': 'tag:BILLING_ROLE','Values': ['Publisher']},
                {'Name': 'instance-state-name','Values':['running']}
                ])
        
        services_instances=client.describe_instances(
            Filters=[
                {'Name': 'tag:BILLING_ENVIRONMENT','Values': ['PRODUCTION']},
                {'Name': 'tag:BILLING_ROLE','Values': ['Services (Tomcat)']},
                {'Name': 'instance-state-name','Values':['running']}
                ])
        
        publisher_instances_count=0
        services_instances_count=0
        backup_publisher_instances_count=0
        
        for reservation in publisher_instances['Reservations']:
            for instance in reservation['Instances']:
                for tags in instance['Tags']:
                    if tags["Key"] == 'Name' and 'backup' in tags["Value"]:
                        backup_publisher_instances_count=backup_publisher_instances_count+1
                        break
                    elif tags["Key"] == 'Name' and 'backup' not in tags["Value"]:
                        publisher_instances_count=publisher_instances_count+1
                        break
				        
				        
                
        for reservation in services_instances['Reservations']:
            services_instances_count=services_instances_count+len(reservation['Instances'])
        
        
        if publisher_instances_count != instance_count[region]['Publisher']:
            if region=='us-east-1':
                Data=str(publisher_instances_count)+ ' Global Publishers running instead of '+str(instance_count[region]['Publisher'])
            else:
                Data=str(publisher_instances_count)+ ' Publishers running in ' +region+' instead of '+str(instance_count[region]['Publisher'])
            notifications.append(Data)
        if services_instances_count != instance_count[region]['Services']:
            Data=str(services_instances_count)+ ' Tomcat instances running in '+region+' instead of '+str(instance_count[region]['Services'])
            notifications.append(Data)
        if backup_publisher_instances_count != instance_count[region]['Publisher Backup']:
            if region=='us-east-1':
                Data=str(backup_publisher_instances_count)+ ' Backup Global Publishers instances running in '+region+' instead of '+str(instance_count[region]['Publisher Backup'])
            else:
                Data=str(backup_publisher_instances_count)+ ' Backup Publishers instances running in '+region+' instead of '+str(instance_count[region]['Publisher Backup'])
                
            notifications.append(Data)
            
    #send_email("Instance Count Notification",'\n\n'.join(notifications))
    if len(notifications) > 0:
        send_email("Instance Count Notification",'Hi All,\n\nFollowing production servers are not in accordance with their required instance count:\n\n'+'\n\n'.join(notifications)+'\n\nRegards,\nHosting team\n\nNote: This is a system generated email do not reply. In case of any issue write to abc@xyz.com')
    else:
        print("All is well")
            
