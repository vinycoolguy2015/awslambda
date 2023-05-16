import boto3,botocore.exceptions
import re


nat_ip=['10.0.10.186','20.10.14.54']
waf_client = boto3.client('wafv2',region_name="us-east-1")
response = waf_client.list_ip_sets(Scope='CLOUDFRONT')
for ipset in response['IPSets']:
	if 'test' in ipset['ARN'] or 'whitelist_ipv4' in ipset['ARN'] or re.search(r'\bipv4\b.*\bwhitelist\b', ipset['ARN']):
		ipset_name=ipset['ARN'].split('/')[-2]
		ipset_id=ipset['ARN'].split('/')[-1]
		nat_ip_exist=[]
		response = waf_client.get_ip_set(Name=ipset_name,Scope='CLOUDFRONT',Id=ipset_id)
		ipsetv4_lock_token=response['LockToken']
		current_ipv4_address=response['IPSet']['Addresses']
		for ip in nat_ip:
			if ip+'/32' in current_ipv4_address:
				nat_ip_exist.append(ip+'/32')
		if len(nat_ip_exist) > 0:
			print(nat_ip_exist,ipset['ARN'].split('/')[-2])
		try:
			waf_client.update_ip_set(Name=ipset_name,Scope='CLOUDFRONT',Id=ipset_id,Addresses=nat_ip_exist,LockToken=ipsetv4_lock_token)
			print("All whitelisted IP addresses except NAT Gateway IP removed from "+ipset_name)
		except botocore.exceptions.ClientError as error:
			print(error.response)
