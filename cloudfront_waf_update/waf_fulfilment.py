import boto3,botocore.exceptions

def fulfilment_handler(event, context):
    client = boto3.client('wafv2',region_name='us-east-1')
    
    
    ipv4=event['currentIntent']['slots']['ipversionfour']
    ipv6=event['currentIntent']['slots']['ipversionsix']
    
    ipsetv4_id=event['sessionAttributes']['ipsetv4_id']
    ipsetv6_id=event['sessionAttributes']['ipsetv6_id']
    ipsetv4_name=event['sessionAttributes']['ipsetv4_name']
    ipsetv6_name=event['sessionAttributes']['ipsetv6_name']
    
    

    try:
       response = client.get_ip_set(Name=ipsetv4_name,Scope='CLOUDFRONT',Id=ipsetv4_id)
       current_ipv4_address=response['IPSet']['Addresses']  
       current_ipv4_address.append(ipv4+'/32')    
       client.update_ip_set(Name=ipsetv4_name,Scope='CLOUDFRONT',Id=ipsetv4_id,Addresses=current_ipv4_address,LockToken=response['LockToken'])
       
       response = client.get_ip_set(Name=ipsetv6_name,Scope='CLOUDFRONT',Id=ipsetv6_id)
       current_ipv6_address=response['IPSet']['Addresses']  
       current_ipv6_address.append(ipv6+'/128')  
       client.update_ip_set(Name=ipsetv6_name,Scope='CLOUDFRONT',Id=ipsetv6_id,Addresses=current_ipv6_address,LockToken=response['LockToken'])
       
       response = {
          "dialogAction": {
               "type": "Close",
                "fulfillmentState": "Fulfilled",
                 "message": {
                    "contentType": "PlainText",
                    "content": (
                        "Thanks, WAF has been updated successfully.")
                   }
               }
           }
    except botocore.exceptions.ClientError as error:
        print(error.response)
        response = {
          "dialogAction": {
               "type": "Close",
                "fulfillmentState": "Fulfilled",
                 "message": {
                    "contentType": "PlainText",
                    "content": (
                        "WAF update failed.Please reach out to DevOps team to update it manually")
                   }
               }
           }
  
    
    
    return response
