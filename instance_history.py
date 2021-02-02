import boto3


from random import seed
from random import randint
import dateutil.parser
import time



def lambda_handler(event, context):
    event_time=event['time']
    instance_id=event['detail']['instance-id']
    instance_state=event['detail']['state']
    seed(time.time())
    event_id = randint(1, 20000000)
   
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('instance_history_details')
    data={}
    data['instance_id'] = instance_id
    data['event_id'] = event_id
    data['instance_state']=instance_state
    data['date']=dateutil.parser.parse(event_time).strftime('%m/%d/%Y')
    data['time']=dateutil.parser.parse(event_time).strftime('%H:%M:%S')
    
    table.put_item(Item=data)
    
        
        
