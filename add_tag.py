import csv
import boto3
from botocore.exceptions import ClientError
with open('test.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    number = 1
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            instance_id=row[0]
            region=row[2]
            purpose=row[7]
            tag=row[6]
            client = boto3.client('ec2',region_name=region)
            try:
               if purpose.strip()!='Validate Purpose':
                  response = client.create_tags(Resources=[instance_id],Tags=[{'Key': 'PURPOSE','Value': tag},{'Key': 'HCR','Value': ''},{'Key': 'COMMENTS','Value': ''}])
                  print ("Tag PURPOSE has been applied to the instance "+instance_id +" with value as "+tag )
               else:
                  response=client.create_tags(Resources=[instance_id],Tags=[{'Key': 'PURPOSE','Value': "PendingValidation"+str(number)},{'Key': 'HCR','Value': ''},{'Key': 'COMMENTS','Value':''}])
                  print ("Tag PURPOSE has been applied to the instance "+instance_id +" with value as PendingValidation"+str(number) )
                  number +=1
            except ClientError as e:
               print e
               #print(instance_id+"does not exist")
            line_count += 1
           
   
