import boto3
import re
client = boto3.client('wafv2',region_name='us-east-1')

ipv4_regex='^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'

ipv6_regex='^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$'

all_ipset_records=[]
response = client.list_ip_sets(Scope='CLOUDFRONT')
ipset_name=[ ipset['Name'] for ipset in response['IPSets'] ]

   
def validate(event,context):
    #if event['sessionAttributes'] is not None:
    session_attributes = event['sessionAttributes']
    #else:
    #    session_attributes = {}
    #    event['sessionAttributes']={}
    slots = event['currentIntent']['slots']
    print("Event Value")
    print(event)
    print("Slot Value")
    print(slots)
    ipsetName = slots['ipsetName'] or None
    
    if slots['ipsetName'] is None:
        
        return {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'ElicitSlot',
                'intentName': event['currentIntent']['name'],
                'slots': slots,
                'slotToElicit': 'ipsetName',
                'message': {'contentType': 'PlainText', 'content':  'Please select an IPSet.Available IPSets are\n'+'\n'.join(ipset_name)}
            }
        }
    if slots['ipsetName'] is not None and slots['ip'] is None:
        if slots['ipsetName'] not in ipset_name:
            
            return {
                'sessionAttributes': session_attributes,
                'dialogAction': {
                    'type': 'ElicitSlot',
                    'intentName': event['currentIntent']['name'],
                    'slots': slots,
                    'slotToElicit': 'ipsetName',
                    'message': {'contentType': 'PlainText', 'content':  'Please select a valid IPSet.Available IPSets are\n '+'\n'.join(ipset_name)}
                }
            }
        else:
            
            return {
                'sessionAttributes': session_attributes,
                'dialogAction': {
                    'type': 'ElicitSlot',
                    'intentName': event['currentIntent']['name'],
                    'slots': slots,
                    'slotToElicit': 'ip',
                    'message': {'contentType': 'PlainText', 'content':  'Please provide IP address'}
                }
            }
    
    if slots['ipsetName'] is not None and slots['ip'] is not None:
        all_ipset_records=[]
        response = client.list_ip_sets(Scope='CLOUDFRONT')
        for ipset in response['IPSets']:
            ipset_record={}
            ipset_record['name']=ipset['Name']
            ipset_record['id']=ipset['Id']
            ipset_record['LockToken']=ipset['LockToken']
            all_ipset_records.append(ipset_record)
        ipset_to_update=slots['ipsetName']
        data=list(filter(lambda record: record['name'] == ipset_to_update, all_ipset_records))
        ipset_id=data[0]['id']
        ipset_lock_token=data[0]['LockToken']
        response = client.get_ip_set(Name=ipset_to_update,Scope='CLOUDFRONT',Id=ipset_id)
        ipAddressVersion=response['IPSet']['IPAddressVersion']
        current_address=response['IPSet']['Addresses']
        address_to_add=slots['ip']
        if ipAddressVersion == 'IPV4':
            match = re.search(ipv4_regex, address_to_add)
            if not match:
                 return {
                    'sessionAttributes': session_attributes,
                    'dialogAction': {
                        'type': 'ElicitSlot',
                        'intentName': event['currentIntent']['name'],
                        'slots': slots,
                        'slotToElicit': 'ip',
                        'message': {'contentType': 'PlainText', 'content': 'Please specify a valid IPV4 IP'}
                    }
                    }
                        
            else:
                print(current_address)
                return {
                'sessionAttributes': {'ipset_id':ipset_id,'ipset_lock_token':ipset_lock_token},
                'dialogAction': {
                    'type': 'Delegate',
                    'slots': slots
                }
            }
                
           
        else: 
            match = re.search(ipv6_regex, address_to_add)
            if not match:
                return {
                    'sessionAttributes': session_attributes,
                    'dialogAction': {
                        'type': 'ElicitSlot',
                        'intentName': event['currentIntent']['name'],
                        'slots': slots,
                        'slotToElicit': 'ip',
                        'message': {'contentType': 'PlainText', 'content': 'Please specify a valid IPV6 IP'}
                        }
                    }
                        
            else:
                return {
                    'sessionAttributes': {'ipset_id':ipset_id,'ipset_lock_token':ipset_lock_token},
                    'dialogAction': {
                        'type': 'Delegate',
                        'slots': slots
                    }
                }

        
        
        
