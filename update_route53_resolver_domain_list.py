import boto3
from datetime import datetime, timedelta
import time
import socket


log_client = boto3.client('logs')
route53_client = boto3.client('route53resolver')

cloudwatch_log_group='/aws/route53/test/dns-firewall'
route53_domain_list='rslvr-fdl-29a70'

response = log_client.start_query(
        logGroupName=cloudwatch_log_group,
        startTime=int((datetime.now() - timedelta(minutes=1440)).timestamp() * 1000),  # Adjust the time range as needed
        endTime=int(datetime.now().timestamp() * 1000),
        queryString="FILTER (firewall_rule_action = 'ALERT' and query_name not like /compute.internal/ and query_name not like /in-addr.arpa/)| stats count(*) by query_name",
    )
query_id = response['queryId']


response = route53_client.list_firewall_domains(FirewallDomainListId='rslvr-fdl-29a703e106e94b53')
domain_name_already_whitelisted=response['Domains']
while True:
    domain_name_to_whitelist=[]
    response = log_client.get_query_results(queryId=query_id)
    if response['status'] == 'Complete':
        results=response['results']
        for record in results:
            domain_name_blocked=record[0]['value'][:-1]
            try:
                addr = socket.gethostbyname_ex(domain_name_blocked)
            except:
                print("Could not resolve "+domain_name_blocked)
            else:
                domain_name_returned=addr[0].split(".")[-2:]
                if domain_name_blocked.split(".")[-2:] == domain_name_returned:
                    wildcard_domain=".".join(domain_name_returned)
                    if "*."+wildcard_domain+'.' not in domain_name_already_whitelisted:
                        domain_name_to_whitelist.append("*."+wildcard_domain)
                else:
                    wildcard_domain=".".join(domain_name_returned)
                    whitelist_blocked_domain=".".join(domain_name_blocked.split(".")[-2:])
                    if "*."+wildcard_domain+'.' not in domain_name_already_whitelisted:
                        domain_name_to_whitelist.append("*."+wildcard_domain)
                    if "*."+whitelist_blocked_domain+'.' not in domain_name_already_whitelisted:   
                        domain_name_to_whitelist.append("*."+whitelist_blocked_domain)
        break
    time.sleep(10)
if len(domain_name_to_whitelist) > 0:
     print(domain_name_to_whitelist)
     route53_client.update_firewall_domains(FirewallDomainListId=route53_domain_list,Operation='ADD',Domains=domain_name_to_whitelist)
else:
    print("No Domain name requires whitelisting")
