def lambda_handler(event, context):
    import boto3
    import datetime
    import time

    
    snsarn='arn:aws:sns:us-east-1:xyz:qasnapshot'
    queueurl='https://sqs.us-east-1.amazonaws.com/xyz/qasnapshot-queue'
    snapshots=[]
   
    
    sqs = boto3.client('sqs')
    REGIONS = ['us-east-1','eu-west-1','ap-northeast-1']
    for region in REGIONS:
        ec = boto3.client('ec2', region_name=region)
        reservations = ec.describe_instances(Filters=[{'Name':'tag:Name', 'Values':['EC2-us-east-1-SingleBoxStack']},{'Name':'instance-state-name','Values':['running']}]).get('Reservations', [])
        instances = sum([[i for i in r['Instances']]for r in reservations], [])
        print ("Number of the Instances in %s region: %d" % (region,len(instances),))
        for instance in instances:
            try:
                retention_days = [int(t.get('Value')) for t in instance['Tags']if t['Key'] == 'Retention'][0]
            except IndexError:
                retention_days = 90
            for dev in instance['BlockDeviceMappings']:
                if dev.get('Ebs', None) is None:
                    continue
                vol_id = dev['Ebs']['VolumeId']
                for name in instance['Tags']:
                    Instancename= name['Value']
                    key= name['Key']
                    if key == 'Name':
                        ins_name = Instancename
                print ("Found EBS volume %s on instance %s" % (vol_id, instance['InstanceId']))
                description="%s_%s" % (ins_name,vol_id)
                snap = ec.create_snapshot(VolumeId=vol_id,Description=description)
                snapshots.append(snap['SnapshotId'])
                snapshotId=snap['SnapshotId']
                print ("%s created" % (snap['Description'],))
                delete_date = datetime.date.today() + datetime.timedelta(days=retention_days)
                snap = snap['Description'] + str('_')
                snapshot = snap + str(datetime.date.today())
                delete_fmt = delete_date.strftime('%Y-%m-%d')
                print ("Will delete snapshots on %s" % (delete_fmt,))
                ec.create_tags(Resources=[snapshotId],Tags=[{'Key': 'Name', 'Value': snapshot},
                    {'Key': 'Instance_ID', 'Value': instance['InstanceId']},
                    {'Key': 'ProdAuth-DeleteOn', 'Value': delete_fmt}])
                			
                response = sqs.send_message(QueueUrl=queueurl,MessageBody='SnapshotData',MessageAttributes={
        'instanceid': {
            'StringValue': instance['InstanceId'],
            'DataType': 'String'
        },
        'snapshotid': {
            'StringValue': snapshotId,
            'DataType': 'String'
        },
        'region': {
            'StringValue': region,
            'DataType': 'String'
        },
        'snapshotname': {
            'StringValue': snapshot,
            'DataType': 'String'
        },
        'deleteon': {
            'StringValue': delete_fmt,
            'DataType': 'String'
        }
    })
    client = boto3.client('sns')
    response = client.publish(TargetArn=snsarn,Message=','.join(snapshots)+" created")




