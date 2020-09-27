from datetime import datetime,timedelta#
#from time import mktime
import dateutil.tz
import time 
import boto3
import collections
import math

#Epoch Function 

eastern = dateutil.tz.gettz('US/Eastern')
dt = datetime.now(tz=eastern)
#dt = datetime.now()
#ddt = datetime.today(tz=eastern) - timedelta(hours=1)
ddt = dt - timedelta(hours=1)
region = 'ap-northeast-1'
#startOfDay = ddt.replace(hour=0, minute=0, second=0, microsecond=0)
#endOfDay = ddt.replace(hour=23, minute=59, second=59, microsecond=999999)


#Function to export logs
def lambda_handler(event, context):

    s3 = boto3.client('logs')
    groupname=['/aws/lambda/function1','/aws/lambda/function2',]
    for i in groupname: 
      time.sleep(10)
      response = s3.create_export_task(
        taskName='export_task',
        logGroupName=i,
        fromTime=math.floor(ddt.timestamp() * 1000),
        to=math.floor(dt.timestamp() * 1000),
        destination='lambda-export',
        #destinationPrefix='AWS'
        destinationPrefix='exportedlogs'
        
     )

    print (response)  
    
