import boto3

def fulfilment_handler(event, context):
    client = boto3.client('ec2',region_name=event['sessionAttributes']['region'])
    volumeId = event['currentIntent']['slots']['instanceDetails']
    

    response = {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": (
                    "Thanks, I have started creating snapshot for {0}."
                ).format(volumeId)
            }
        }
    }
    client.create_snapshot(VolumeId=volumeId,Description=volumeId+"_Snap")
    return response
