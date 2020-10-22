import boto3

def get_all_regions():
    client = boto3.client('ec2')
    regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    return regions
    
def get_all_instances(region):
    client = boto3.resource('ec2',region_name=region)
    instances=[instance.id for instance in client.instances.all()]
    return instances

def get_instance_volumes(region,instance):
    client = boto3.resource('ec2', region_name=region)
    volume_data = client.Instance(instance).volumes.all()
    volumes=[v.id for v in volume_data]
    return volumes

def validate(event,context):
    if event['sessionAttributes'] is not None:
        session_attributes = event['sessionAttributes']
    else:
        session_attributes = {}
        event['sessionAttributes']={}
    slots = event['currentIntent']['slots']
    instance_detail = slots['instanceDetails'] or ''
    if instance_detail.lower() == 'help':
        return {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'ElicitSlot',
                'intentName': event['currentIntent']['name'],
                'slots': slots,
                'slotToElicit': 'instanceDetails',
                'message': {'contentType': 'PlainText', 'content': 'In order to take snapshot of an instance, you need to specify the region first.After this,all the instances running in that region will be listed.Next specify the instance you want to take snapshot of,and all the volumes attached to the instance will belisted.You can specify a specific volume or all the volumes to take snapshot of.'}
            }
        }
        
    if 'instance' not in event['sessionAttributes']:
        if 'region' not in event['sessionAttributes']:
            if instance_detail.lower() not in get_all_regions():
                return {
                    'sessionAttributes': session_attributes,
                    'dialogAction': {
                        'type': 'ElicitSlot',
                        'intentName': event['currentIntent']['name'],
                        'slots': slots,
                        'slotToElicit': 'instanceDetails',
                        'message': {'contentType': 'PlainText', 'content': 'Please select a valid region.Available regions are '+','.join(get_all_regions())}
                    }
                }
            else:
                instances=get_all_instances(instance_detail.lower())
                event['sessionAttributes']['region']=instance_detail
                if len(instances)>0:
                    return {
                        'sessionAttributes': session_attributes,
                        'dialogAction': {
                            'type': 'ElicitSlot',
                            'intentName': event['currentIntent']['name'],
                            'slots': slots,
                            'slotToElicit': 'instanceDetails',
                            'message': {'contentType': 'PlainText', 'content': 'Please specify an instance.Available instances are '+','.join(instances)}
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
                            'slotToElicit': 'instanceDetails',
                            'message': {'contentType': 'PlainText', 'content': 'No instance running in the specified region.Select another region.'}
                        }
                    }
        else:
            instances=get_all_instances(event['sessionAttributes']['region'].lower())
            if instance_detail not in instances:
                return {
                        'sessionAttributes': session_attributes,
                        'dialogAction': {
                            'type': 'ElicitSlot',
                            'intentName': event['currentIntent']['name'],
                            'slots': slots,
                            'slotToElicit': 'instanceDetails',
                            'message': {'contentType': 'PlainText', 'content': 'Please specify a valid instance.Available instances are '+','.join(instances)}
                            }
                        }
            else:
                event['sessionAttributes']['instance']=instance_detail
                volumes=get_instance_volumes(event['sessionAttributes']['region'],instance_detail)
                return {
                        'sessionAttributes': session_attributes,
                        'dialogAction': {
                            'type': 'ElicitSlot',
                            'intentName': event['currentIntent']['name'],
                            'slots': slots,
                            'slotToElicit': 'instanceDetails',
                            'message': {'contentType': 'PlainText', 'content': 'Please specify a volume.Available volumes are '+','.join(volumes)}
                            }
                        }
            
    else:
        volumes=get_instance_volumes(event['sessionAttributes']['region'],event['sessionAttributes']['instance'])
        if instance_detail not in volumes:
            return {
                    'sessionAttributes': session_attributes,
                    'dialogAction': {
                        'type': 'ElicitSlot',
                        'intentName': event['currentIntent']['name'],
                        'slots': slots,
                        'slotToElicit': 'instanceDetails',
                        'message': {'contentType': 'PlainText', 'content': 'Please specify a valid volume.Available volumes are '+','.join(volumes)}
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



       
       
        
