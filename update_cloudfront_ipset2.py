#python3 ~/Documents/update_cloudfront_ipset2.py google.com 10.10.10.10 2a09:bac1:8560:8::24:1bb

import boto3,botocore.exceptions
import re
import sys

client = boto3.client('cloudfront')
waf_client = boto3.client('wafv2',region_name="us-east-1")
domain=sys.argv[1]
ipv4_to_add=sys.argv[2]
ipv6_to_add=sys.argv[3]
distribution_id=''
ipv4_rule_set=''
ipv6_rule_set=''

ipv4_regex='^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'

ipv6_regex='^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$'

response = client.list_distributions()
for distribution in response['DistributionList']['Items']:
   if distribution['Aliases']['Quantity'] > 0:
      if domain in distribution['Aliases']['Items']:
         distribution_id=distribution['Id']
         break
         
response = client.get_distribution_config(Id=distribution_id)
web_acl_arn=response['DistributionConfig']['WebACLId']
web_acl_id=web_acl_arn.split('/')[-1]
web_acl_name=web_acl_arn.split('/')[-2]

response = waf_client.get_web_acl(Name=web_acl_name,Scope='CLOUDFRONT',Id=web_acl_id)
for rule in response['WebACL']['Rules']:
   if rule['Name'] == 'default-whitelist_ipv4_cidr-rule':
      ipv4_rule_set=str(rule['Statement']['IPSetReferenceStatement']['ARN'])
   if rule['Name'] == 'default-whitelist_ipv6_cidr-rule':
      ipv6_rule_set=str(rule['Statement']['IPSetReferenceStatement']['ARN'])

response = waf_client.get_ip_set(
    Name=ipv4_rule_set.split('/')[-2],
    Scope='CLOUDFRONT',
    Id=ipv4_rule_set.split('/')[-1]
)
ipsetv4_lock_token=response['LockToken']
current_ipv4_address=response['IPSet']['Addresses']
match = re.search(ipv4_regex, ipv4_to_add)
if match:
   print('Valid IPv4 Address')
   current_ipv4_address.append(ipv4_to_add+'/32')
   try:
      response = waf_client.update_ip_set(Name=ipv4_rule_set.split('/')[-2],Scope='CLOUDFRONT',Id=ipv4_rule_set.split('/')[-1],Addresses=current_ipv4_address,LockToken=ipsetv4_lock_token)
      print("IPV4 Address Added")
   except botocore.exceptions.ClientError as error:
      print(error.response)   
else:
   print('Invalid IPv4 Address')


response = waf_client.get_ip_set(
    Name=ipv6_rule_set.split('/')[-2],
    Scope='CLOUDFRONT',
    Id=ipv6_rule_set.split('/')[-1]
)
ipsetv6_lock_token=response['LockToken']
current_ipv6_address=response['IPSet']['Addresses']
match = re.search(ipv6_regex, ipv6_to_add)
if match:
   print('Valid IPv6 Address')
   current_ipv6_address.append(ipv6_to_add+'/128')
   try:
      response = waf_client.update_ip_set(Name=ipv6_rule_set.split('/')[-2],Scope='CLOUDFRONT',Id=ipv6_rule_set.split('/')[-1],Addresses=current_ipv6_address,LockToken=ipsetv6_lock_token)
      print("IPV6 Address Added")
   except botocore.exceptions.ClientError as error:
      print(error.response)
else:
   print('Invalid IPv6 Address')

    


