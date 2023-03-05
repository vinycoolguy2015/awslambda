import boto3

def fulfilment_handler(event, context):
    client = boto3.client('wafv2',region_name='us-east-1')
    ipsetname = event['currentIntent']['slots']['ipsetName']
    ip=event['currentIntent']['slots']['ip']
    ipset_id=event['sessionAttributes']['ipset_id']
    ipset_lock_token=event['sessionAttributes']['ipset_lock_token']
    
    response = client.get_ip_set(Name=ipsetname,Scope='CLOUDFRONT',Id=ipset_id)
    current_address=response['IPSet']['Addresses']  
    ipAddressVersion=response['IPSet']['IPAddressVersion']
    address_to_add=ip

    if ipAddressVersion == 'IPV4':
        current_address.append(address_to_add+'/32')
        client.update_ip_set(Name=ipsetname,Scope='CLOUDFRONT',Id=ipset_id,Addresses=current_address,LockToken=ipset_lock_token)
        response = {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": (
                        "Thanks, IPSet Update Successfully.")
                }
            }
        }
  
    else: 
        current_address.append(address_to_add+'/128')
        client.update_ip_set(Name=ipsetname,Scope='CLOUDFRONT',Id=ipset_id,Addresses=current_address,LockToken=ipset_lock_token)
  
        response = {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": (
                        "Thanks, IPSet Updated Successfully.")
                }
            }
        }
    
    return response
