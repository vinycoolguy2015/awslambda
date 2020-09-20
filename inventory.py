import boto3
import csv
import sys
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
    msg.preamble = 'Inventory Report\n'
    part = MIMEText('Hi All,\nPFA Inventory report with host added or removed Summery.  \n\nRegards, \nDevOps team \nNote: This is a system generated email do not reply. In case of any issue write to abc@abc.com. ')
    msg.attach(part)
    part = MIMEApplication(open(attachment, 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename=attachment.split('/')[-1])
    msg.attach(part)
    result = client.send_raw_email(
        RawMessage={'Data': msg.as_string()},
        Source=msg['From'],
        Destinations=[msg['To']])

def lambda_handler(event, context):
    previous_inventory = set()
    current_inventory=set()
    previous_inventory_complete_data={}
    current_inventory_complete_data={}
    
    previous_day=datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
    
    s3_client = boto3.client('s3')
    s3_bucket='nissan-inventory'
    current_inventory_file=event['Records'][0]['s3']['object']['key']
    previous_day_inventory_file="EC2_Inventory_"+previous_day.split('-')[0]+"_"+previous_day.split('-')[1]+"_"+previous_day.split('-')[2]+".csv"
    output_file='/tmp/AddOrRemovedHost_report_'+datetime.today().strftime('%Y-%m-%d')+'.csv'
    
    s3_client.download_file(s3_bucket, current_inventory_file,'/tmp/'+current_inventory_file)
    s3_client.download_file(s3_bucket,previous_day_inventory_file,'/tmp/'+previous_day_inventory_file)
    
    
    with open("/tmp/"+previous_day_inventory_file) as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for row in reader:
            previous_inventory.add((row['Instance_Name'].strip()+"_"+row['PrivateIpAddress'].strip()))
            previous_inventory_complete_data[row['Instance_Name'].strip()+"_"+row['PrivateIpAddress'].strip()] = {}
            previous_inventory_complete_data[row['Instance_Name'].strip()+"_"+row['PrivateIpAddress'].strip()]['Instance_Type']= row['Instance_Type'].strip()
            previous_inventory_complete_data[row['Instance_Name'].strip()+"_"+row['PrivateIpAddress'].strip()]["UniqueID"]= row['Tag:UniqueID'].strip()
            



    with open("/tmp/"+current_inventory_file) as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for row in reader:
            current_inventory.add((row['Instance_Name'].strip()+"_"+row['PrivateIpAddress'].strip()))
            current_inventory_complete_data[row['Instance_Name'].strip()+"_"+row['PrivateIpAddress'].strip()] = {}
            current_inventory_complete_data[row['Instance_Name'].strip()+"_"+row['PrivateIpAddress'].strip()]['Instance_Type']= row['Instance_Type'].strip()
            current_inventory_complete_data[row['Instance_Name'].strip()+"_"+row['PrivateIpAddress'].strip()]["UniqueID"]= row['Tag:UniqueID'].strip()
        
    instances_terminated=previous_inventory.difference(current_inventory)
    instances_launched=current_inventory.difference(previous_inventory)
    
    if not instances_terminated and not instances_launched:
        print("No change detected")
        sys.exit(1)

    csv_file = open(output_file,'w+')
    csv_file.write("Instance_Name,Instance_IP,Instance_Type,Instance_Unique_Tag,Action\n\n")

    for instance in instances_terminated:
        csv_file.write("%s,%s,%s,%s,%s\n"%(
								instance.split("_")[0],
				                instance.split("_")[-1],
				                previous_inventory_complete_data[instance]['Instance_Type'],
				                previous_inventory_complete_data[instance]['UniqueID'],
								"Terminated"
								
				))
    for instance in instances_launched:
        csv_file.write("%s,%s,%s,%s,%s\n"%(
								instance.split("_")[0],
				                instance.split("_")[-1],
				                current_inventory_complete_data[instance]['Instance_Type'],
				                current_inventory_complete_data[instance]['UniqueID'],
								"Launched"
								
				))
    csv_file.flush()
    previous_day_inventory_file="/tmp/"+previous_day_inventory_file
    current_inventory_file="/tmp/"+current_inventory_file
    send_report("Add_or_Remove_Summary","abc@abc,com","abc@abc.com",output_file)
				


