import boto3
import re
waf_client = boto3.client('wafv2',region_name='us-east-1')
cloudfront_client = boto3.client('cloudfront')


ipv4_regex='^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'

ipv6_regex='^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$'

all_domains=[]
response = cloudfront_client.list_distributions()
for distribution in response['DistributionList']['Items']:
   all_domains.append(distribution['DomainName'])
   
#For Alias You can Use
#for distribution in response['DistributionList']['Items']:
#   if distribution['Aliases']['Quantity'] > 0:
#      for domain in distribution['Aliases']['Items']:
#         all_domains.append(domain)



   
def validate(event,context):
    distribution_id=''
    ipv4_rule_set=''
    ipv6_rule_set=''
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
    cloudfront_url = slots['cloudfront'] or None
    
    if slots['cloudfront'] is None:
        
        return {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'ElicitSlot',
                'intentName': event['currentIntent']['name'],
                'slots': slots,
                'slotToElicit': 'cloudfront',
                'message': {'contentType': 'PlainText', 'content':  'Please specify a URL.Available URLs are\n'+'\n'.join(all_domains)}
            }
        }
    if slots['cloudfront'] is not None and slots['ipversionfour'] is None:
        
        if slots['cloudfront']+'.cloudfront.net' not in all_domains:
        
            
            return {
                'sessionAttributes': session_attributes,
                'dialogAction': {
                    'type': 'ElicitSlot',
                    'intentName': event['currentIntent']['name'],
                    'slots': slots,
                    'slotToElicit': 'cloudfront',
                    'message': {'contentType': 'PlainText', 'content':  'Please specify a URL.Available URLs are\n'+'\n'.join(all_domains)}
                }
            }
        else:
            
            return {
                'sessionAttributes': session_attributes,
                'dialogAction': {
                    'type': 'ElicitSlot',
                    'intentName': event['currentIntent']['name'],
                    'slots': slots,
                    'slotToElicit': 'ipversionfour',
                    'message': {'contentType': 'PlainText', 'content':  'Please provide IPV4 address'}
                }
            }
            
    if slots['cloudfront'] is not None and slots['ipversionfour'] is not None and slots['ipversionsix'] is None:
        match = re.search(ipv4_regex, slots['ipversionfour'])
        if not match:
            return {
                'sessionAttributes': session_attributes,
                'dialogAction': {
                'type': 'ElicitSlot',
                'intentName': event['currentIntent']['name'],
                'slots': slots,
                'slotToElicit': 'ipversionsix',
                'message': {'contentType': 'PlainText', 'content': 'Please specify a valid IPV4 IP'}
                }
                    }
        else:
            return {
                'sessionAttributes': session_attributes,
                'dialogAction': {
                    'type': 'ElicitSlot',
                    'intentName': event['currentIntent']['name'],
                    'slots': slots,
                    'slotToElicit': 'ipversionsix',
                    'message': {'contentType': 'PlainText', 'content':  'Please provide IPV6 address'}
                }
            }
    
    if slots['cloudfront'] is not None and slots['ipversionfour'] is not None and slots['ipversionsix'] is not None:
        match = re.search(ipv6_regex, slots['ipversionsix'])
        if not match:
            return {
                'sessionAttributes': session_attributes,
                'dialogAction': {
                'type': 'ElicitSlot',
                'intentName': event['currentIntent']['name'],
                'slots': slots,
                'slotToElicit': 'ipversionfour',
                'message': {'contentType': 'PlainText', 'content': 'Please specify a valid IPV6 IP'}
                }
                    }
        else:
           ipv4_to_add=slots['ipversionfour']
           domain=slots['cloudfront']
           ipv6_to_add=slots['ipversionsix']
        
           response = cloudfront_client.list_distributions()
           for distribution in response['DistributionList']['Items']:
              if distribution['DomainName'] == domain+'.cloudfront.net':
                 distribution_id=distribution['Id']
                 break
           response = cloudfront_client.get_distribution_config(Id=distribution_id)
           web_acl_arn=response['DistributionConfig']['WebACLId']
           web_acl_id=web_acl_arn.split('/')[-1]
           web_acl_name=web_acl_arn.split('/')[-2]

           response = waf_client.get_web_acl(Name=web_acl_name,Scope='CLOUDFRONT',Id=web_acl_id)
           for rule in response['WebACL']['Rules']:
              if rule['Name'] == 'default-whitelist_ipv4_cidr-rule':
                 ipv4_rule_set=str(rule['Statement']['IPSetReferenceStatement']['ARN'])
              if rule['Name'] == 'default-whitelist_ipv6_cidr-rule':
                 ipv6_rule_set=str(rule['Statement']['IPSetReferenceStatement']['ARN'])

           #response = waf_client.get_ip_set(Name=ipv4_rule_set.split('/')[-2],Scope='CLOUDFRONT',Id=ipv4_rule_set.split('/')[-1])
           #ipsetv4_lock_token=response['LockToken']
           ipsetv4_id=ipv4_rule_set.split('/')[-1]
           ipsetv4_name=ipv4_rule_set.split('/')[-2]
           
           #response = waf_client.get_ip_set(Name=ipv6_rule_set.split('/')[-2],Scope='CLOUDFRONT',Id=ipv6_rule_set.split('/')[-1])
           #ipsetv6_lock_token=response['LockToken']
           ipsetv6_id=ipv6_rule_set.split('/')[-1]
           ipsetv6_name=ipv6_rule_set.split('/')[-2]
           
           return {
                'sessionAttributes': {'ipsetv4_id':ipsetv4_id,'ipsetv4_name':ipsetv4_name,'ipsetv6_id':ipsetv6_id,'ipsetv6_name':ipsetv6_name},
                'dialogAction': {'type': 'Delegate','slots': slots}
            }
                
           
        

        
        
        
