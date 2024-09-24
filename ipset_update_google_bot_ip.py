import boto3
import botocore.exceptions
import urllib3
import json


WHITELISTED_IP=['8.8.8.8/8']

waf_client = boto3.client('wafv2',region_name='us-east-1')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://developers.google.com/static/search/apis/ipranges/googlebot.json"
http = urllib3.PoolManager(cert_reqs='CERT_NONE')
response = http.request('GET', url)
data = json.loads(response.data.decode('utf-8'))

ipv4_prefixes = [item['ipv4Prefix'] for item in data['prefixes'] if 'ipv4Prefix' in item]
ipv6_prefixes = [item['ipv6Prefix'] for item in data['prefixes'] if 'ipv6Prefix' in item]
    
ipv4_ip_set='whitelist_ipv4_cidr'
ipv6_ip_set='whitelist_ipv6_cidr'


#IPv4 IPSet    
response = waf_client.get_ip_set(Name= ipv4_ip_set,Scope='CLOUDFRONT',Id='8a335cd6')
ipsetv4_lock_token=response['LockToken']
current_ipv4_address=list(set(response['IPSet']['Addresses']) - set(WHITELISTED_IP))
updated_ip_set=current_ipv4_address+WHITELISTED_IP
ip_address_to_remove = list(set(current_ipv4_address) - set(ipv4_prefixes))
ip_address_to_add = list(set(ipv4_prefixes) - set(current_ipv4_address))
if ip_address_to_remove:
	print("We need to remove some IPv4s from the IPSet "+','.join(ip_address_to_remove))
	updated_ip_set=list(set(current_ipv4_address) - set(ip_address_to_remove))
else:
	print("No IPv4 address to remove from the IPSet")
if ip_address_to_add:
	print("We need to add some IPv4s into the IPSet" +','.join(ip_address_to_add))
	updated_ip_set=updated_ip_set+ip_address_to_add
else:
	print("No IPv4 address to add into the IPSet")

if ip_address_to_add or ip_address_to_remove:
	try:
		response = waf_client.update_ip_set(Name=ipv4_ip_set,Scope='CLOUDFRONT',Id='8a335cd6',Addresses=updated_ip_set,LockToken=ipsetv4_lock_token)
		print("IPv4 IPSet updated")
	except botocore.exceptions.ClientError as error:
		print("Error updating IPv4 IPset. Please reach out to DevOps team")

#IPv6 IPSet    
response = waf_client.get_ip_set(Name= ipv6_ip_set,Scope='CLOUDFRONT',Id='52ff4797')
ipsetv6_lock_token=response['LockToken']
current_ipv6_address=list(set(response['IPSet']['Addresses']))
updated_ip_set=current_ipv4_address
ip_address_to_remove = list(set(current_ipv6_address) - set(ipv6_prefixes))
ip_address_to_add = list(set(ipv6_prefixes) - set(current_ipv6_address))
if ip_address_to_remove:
	print("We need to remove some IPv6s from the IPSet "+','.join(ip_address_to_remove))
	updated_ip_set=list(set(current_ipv6_address) - set(ip_address_to_remove))
else:
	print("No IPv6 address to remove from the IPSet")
if ip_address_to_add:
	print("We need to add some IPv6s into the IPSet " +','.join(ip_address_to_add))
	updated_ip_set=updated_ip_set+ip_address_to_add
else:
	print("No IPv6 address to add into the IPSet")

if ip_address_to_add or ip_address_to_remove:
	try:
		response = waf_client.update_ip_set(Name=ipv6_ip_set,Scope='CLOUDFRONT',Id='52ff4797',Addresses=updated_ip_set,LockToken=ipsetv6_lock_token)
		print("IPv6 IPSet updated")
	except botocore.exceptions.ClientError as error:
		print("Error updating IPv6 IPset. Please reach out to DevOps team")
