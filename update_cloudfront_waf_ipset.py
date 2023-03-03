import boto3
import re

client = boto3.client('wafv2',region_name='us-east-1')

ipv4_regex='^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'

ipv6_regex='^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$'

all_ipset_records=[]

response = client.list_ip_sets(Scope='CLOUDFRONT')

for ipset in response['IPSets']:
  ipset_record={}
  ipset_record['name']=ipset['Name']
  ipset_record['id']=ipset['Id']
  ipset_record['LockToken']=ipset['LockToken']
  all_ipset_records.append(ipset_record)
 
ipset_to_update='v6'
data=list(filter(lambda record: record['name'] == ipset_to_update, all_ipset_records))
ipset_id=data[0]['id']
ipset_lock_token=data[0]['LockToken']

response = client.get_ip_set(
    Name=ipset_to_update,
    Scope='CLOUDFRONT',
    Id=ipset_id
)
ipAddressVersion=response['IPSet']['IPAddressVersion']
current_address=response['IPSet']['Addresses']
address_to_add='2a09:bac2:3520:8::23:323'

if ipAddressVersion == 'IPV4':
  match = re.search(ipv4_regex, address_to_add)
  if match:
    current_address.append(address_to_add+'/32')
    response = client.update_ip_set(Name=ipset_to_update,Scope='CLOUDFRONT',Id=ipset_id,Addresses=current_address,LockToken=ipset_lock_token)
  else:
    print('Invalid IPv4 Address')
else: 
  match = re.search(ipv6_regex, address_to_add)
  if match:
    current_address.append(address_to_add+'/128')
    response = client.update_ip_set(Name=ipset_to_update,Scope='CLOUDFRONT',Id=ipset_id,Addresses=current_address,LockToken=ipset_lock_token)
  else:
    print('Invalid IPv6 Address')
