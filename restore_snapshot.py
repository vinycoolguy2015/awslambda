import boto3

client = boto3.client('ec2',region_name='ap-south-1')
volume='vol-xyz' 

snapshots= client.describe_snapshots(
     Filters=[
        {
            'Name': 'volume-id',
            'Values': [
               volume,
            ]
        },
    ],
    OwnerIds=[
        'xyz',
    ],
    MaxResults=100
)
snapshot=snapshots['Snapshots'][0]
print "Check if date of snapshot is current date or current date -1. Snapshot date: "+str(snapshot['StartTime'])
raw_input("Press Enter to continue...")
instance_id=raw_input("Enter new server's instance id")
response = client.describe_instances(

    InstanceIds=[
        instance_id
    ]
)
az=response['Reservations'][0]['Instances'][0]['Placement']['AvailabilityZone']
print "Creating volume.Hold on for a minute"
response = client.create_volume(Encrypted=True,SnapshotId=snapshot['SnapshotId'],AvailabilityZone=az)
waiter = client.get_waiter('volume_available')
waiter.wait(
    VolumeIds=[
        response['VolumeId']
    ],
    WaiterConfig={
        'Delay': 15,
        'MaxAttempts': 100
    }
)
print "Volume "+response['VolumeId']+ " created."

attach_volume_response=client.attach_volume(
    Device='/dev/sdy',
    InstanceId=instance_id,
    VolumeId=response['VolumeId']
)
print "Volume attached to the instance"
