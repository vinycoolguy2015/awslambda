import boto3

def fullfilment_handler(event, context):
    client = boto3.client('rds',region_name=event['sessionAttributes']['region'])
    rds_instance = event['currentIntent']['slots']['dbInstanceIdentifier']
    

    response = {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": (
                    "Thanks, I have started creating snapshot for {0}."
                ).format(rds_instance)
            }
        }
    }
    client.create_db_snapshot(  DBInstanceIdentifier=rds_instance,
                                DBSnapshotIdentifier=rds_instance+'-Snapshot',
                                Tags=[
                                    {
                                    'Key': 'Name',
                                    'Value': rds_instance+'_Snapshot'
                                }
                            ]
                        )
    return response
