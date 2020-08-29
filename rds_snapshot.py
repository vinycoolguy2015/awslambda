def lambda_handler(event, context):
    import boto3
    import time
    import datetime
    d = datetime.datetime.today()
    suffix=d.strftime('%d-%m-%Y')
    DBSnapshotIdentifier='prod-snapshot'+suffix
    client = boto3.client('rds')
    sns_client = boto3.client('sns')

    client.create_db_snapshot(DBSnapshotIdentifier=DBSnapshotIdentifier,DBInstanceIdentifier='prod')
    time.sleep(300)
    while True:
        response = client.describe_db_snapshots(DBSnapshotIdentifier=DBSnapshotIdentifier)
        if response['DBSnapshots'][0]['Status'] =='available':
            message= "Snapshot created"
            response = sns_client.publish(TopicArn='',Message=message,Subject='RDS Snapshot Status')
            break
        if context.get_remaining_time_in_millis() < 10000:
            message="Snapshot creation is still in progress"+response['DBSnapshots'][0]['PercentProgress']
            response = sns_client.publish(TopicArn='',Message=message,Subject='RDS Snapshot Status')
            break
        time.sleep(5)
