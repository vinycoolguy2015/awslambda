import boto3
import re
waf_client = boto3.client('wafv2',region_name='us-east-1')
cloudfront_client = boto3.client('cloudfront')


ipv4_regex='^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'

ipv6_regex='^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$'


def lambda_handler(event,context):
    distribution_id=None
    ipv4_rule_set=''
    ipv6_rule_set=''
    ipv4_to_add=event['ipv4']
    domain=event['domain']
    ipv6_to_add=event['ipv6']
    
    response = cloudfront_client.list_distributions()
    for distribution in response['DistributionList']['Items']:
        if distribution['DomainName'] == domain+'.cloudfront.net':
            distribution_id=distribution['Id']
            break
    
    #for distribution in response['DistributionList']['Items']:
    #    if distribution['Aliases']['Quantity'] > 0:
    #        if domain in distribution['Aliases']['Items']:
    #            distribution_id=distribution['Id']
    #            break
                
    if distribution_id is None:
        return {'message': "No CloudFront distribution found for this domain name."}
         
    response = cloudfront_client.get_distribution_config(Id=distribution_id)
    web_acl_arn=response['DistributionConfig']['WebACLId']
    web_acl_id=web_acl_arn.split('/')[-1]
    web_acl_name=web_acl_arn.split('/')[-2]
    if re.search(r'\bopen\b.*\b', web_acl_name):
        return {'message': web_acl_name+" does not need whitelisting."}
    
   
    response = waf_client.get_web_acl(Name=web_acl_name,Scope='CLOUDFRONT',Id=web_acl_id)
    for rule in response['WebACL']['Rules']:
        if rule['Name'] == 'default-whitelist_ipv4_cidr-rule' or rule['Name'] == 'default-ipv4-white-list' or re.search(r'\bipv4\b.*\bwhitelist\b', rule['Name']):
            ipv4_rule_set=str(rule['Statement']['IPSetReferenceStatement']['ARN'])
        if rule['Name'] == 'default-whitelist_ipv6_cidr-rule' or rule['Name'] == 'default-ipv6-whitelist' or re.search(r'\bipv6\b.*\bwhitelist\b', rule['Name']):
            ipv6_rule_set=str(rule['Statement']['IPSetReferenceStatement']['ARN'])

    response = waf_client.get_ip_set(Name=ipv4_rule_set.split('/')[-2],Scope='CLOUDFRONT',Id=ipv4_rule_set.split('/')[-1])

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
            return {'message': "Error updating WAF. Please reach out to DevOps team"}
            
    else:
        return {'message': "Invalid IPV4 address provided."}

    if ipv6_to_add != "None":
        response = waf_client.get_ip_set(Name=ipv6_rule_set.split('/')[-2],Scope='CLOUDFRONT',Id=ipv6_rule_set.split('/')[-1])
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
                return {'message': "Error updating WAF. Please reach out to DevOps team"}
        else:
            return {'message': "Invalid IPV6 address provided."}
            
    return {'message': "WAF is updated."}
