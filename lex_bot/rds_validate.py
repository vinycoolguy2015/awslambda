import boto3

def get_all_regions():
    client = boto3.client('ec2')
    regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    return regions
    
def get_rds_instances(region):
    client = boto3.client('rds',region_name=region)
    response = client.describe_db_instances()
    instances=[instance['DBInstanceIdentifier'] for instance in response['DBInstances']]
    return instances


def lambda_handler(event,context):
    if event['sessionAttributes'] is not None:
        session_attributes = event['sessionAttributes']
    else:
        session_attributes = {}
    slots = event['currentIntent']['slots']
    region = slots['region'] or ''
    dbInstanceIdentifier = slots['dbInstanceIdentifier'] or ''
    if 'region' not in event['sessionAttributes']:
        if region.lower() not in get_all_regions():
            return {
                'sessionAttributes': session_attributes,
                'dialogAction': {
                    'type': 'ElicitSlot',
                    'intentName': event['currentIntent']['name'],
                    'slots': slots,
                    'slotToElicit': 'region',
                    'message': {'contentType': 'PlainText', 'content': 'Please select a valid region.Available regions are '+','.join(get_all_regions())}
                }
            }
        else:
            event['sessionAttributes']['region']=region
            rds_instances=get_rds_instances(region)
            
            if len(rds_instances)>0:
                return {
                    'sessionAttributes': session_attributes,
                    'dialogAction': {
                        'type': 'ElicitSlot',
                        'intentName': event['currentIntent']['name'],
                        'slots': slots,
                        'slotToElicit': 'dbInstanceIdentifier',
                        'message': {'contentType': 'PlainText', 'content': 'Please specify a RDS instance.Available instances are '+','.join(rds_instances)}
                        }
                    }
            else:
                event['sessionAttributes'].pop('region')
                return {
                    'sessionAttributes': session_attributes,
                    'dialogAction': {
                        'type': 'ElicitSlot',
                        'intentName': event['currentIntent']['name'],
                        'slots': slots,
                        'slotToElicit': 'region',
                        'message': {'contentType': 'PlainText', 'content': 'No RDS instance running in the specified region.Select another region.'}
                    }
                }
    else:
        if dbInstanceIdentifier not in get_rds_instances(region):
            return {
                'sessionAttributes': session_attributes,
                'dialogAction': {
                    'type': 'ElicitSlot',
                    'intentName': event['currentIntent']['name'],
                    'slots': slots,
                    'slotToElicit': 'dbInstanceIdentifier',
                    'message': {'contentType': 'PlainText', 'content': 'Please select a valid RDS instance.Available RDS instances are: '+','.join(get_rds_instances(region))}
                }
            }
        else:
        
            return {
                'sessionAttributes': session_attributes,
                'dialogAction': {
                    'type': 'Delegate',
                    'slots': slots
                }
            }
        
        
        
    
                        
            
   
            



       
       
        
