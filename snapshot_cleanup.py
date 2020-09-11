import boto3
import re
from datetime import datetime,timedelta
from botocore.exceptions import ClientError
import boto3.session

def check_volume(volume_id):
    if not volume_id: return ''
    try:
        volume=client.describe_volumes(VolumeIds=[volume_id])
        if not volume['Volumes'][0]['VolumeId']:
            return False
        return True
    except ClientError:
        return False

def check_ami(image_id):
    if not image_id: return ''
    try:
        image= client.describe_images(ImageIds=[image_id])
        if not image['Images']:
            return False
        else:
            if 'prod' in image['Images'][0]['Name']:
                return 'Prod'
            else:
                return 'NonProd'
    except ClientError:
        return False


def get_snapshot_age(snapshot_id):
    try:
        response = client.describe_snapshots(SnapshotIds=[snapshot_id])
        start_time=response['Snapshots'][0]['StartTime']
        #current_date = datetime.datetime.strptime(str(datetime.date.today()), date_format)
        #snapshot_creation_date = datetime.datetime.strptime(start_time, date_format)
        current_date = datetime.now()
        snapshot_age = (current_date-(start_time.replace(tzinfo=None))).days
        return snapshot_age
    except ClientError:
        return False



def get_ami(snapshot_description):
    regex = r"^Created by CreateImage\((.*?)\) for (.*?) "
    parsed_data = re.findall(regex, snapshot_description, re.MULTILINE)
    if len(parsed_data)>0:
        ami_id= parsed_data[0][1]
        return ami_id
    else:
        return False


def get_snapshot_type(snapshot_name,snapshot_description,snapshot_billing_environment):
    if 'grafana' in snapshot_name.lower().strip():
        snapshot_type='Prod'
        return snapshot_type
    if not snapshot_billing_environment:
        if not snapshot_name:
            if not snapshot_description:
                snapshot_type='NonProd'
            else:
                if 'prod' in snapshot_description:
                    snapshot_type='Prod'
                else:
                    snapshot_type='NonProd'
        else:
            if 'prod' in snapshot_name:
                snapshot_type='Prod'
            else:
                snapshot_type='NonProd'
    else:
        pattern = '^prod'
        result = re.match(pattern,snapshot_billing_environment.lower().strip())
        if result:
            snapshot_type='Prod'
        else:
            snapshot_type='NonProd'
    return snapshot_type

def get_retention_period(ami_exists,volume_exists,snapshot_type):
    retention_days=''
    if not ami_exists and not volume_exists:
        if snapshot_type=="Prod":
            retention_days=180
        else:
            retention_days=90
    else:
        if snapshot_type=="NonProd":
            retention_days=180
        else:
            retention_days=390
    return retention_days





#regions=['us-east-1']
profile='account1'
regions=['us-east-1','ap-northeast-1','eu-west-1']
session= boto3.session.Session(profile_name=profile)
for region in regions:
    client = session.client('ec2',region_name=region)
    #response = client.describe_snapshots(OwnerIds=['xxxxx']) #account1
    response = client.describe_snapshots(OwnerIds=['xxxxxxx']) #account2
    for snapshot in response['Snapshots']:
        snapshot_name=''
        snapshot_description =''
        snapshot_billing_environment=''
        mark_for_deletion=False
        if 'Tags' in snapshot:
            for tags in snapshot['Tags']:
                if tags["Key"] == 'Name':
                    snapshot_name = tags["Value"]
                if tags["Key"] == 'BILLING_ENVIRONMENT':
                    snapshot_billing_environment = tags["Value"]

        snapshot_description=snapshot['Description']
        ami_id=get_ami(snapshot_description)
        if ami_id:
            snapshot_type=check_ami(ami_id)
            if snapshot_type==False:
                snapshot_type='Undetermined'
                ami_exists=False
            else:
                ami_exists=True
        else:
            snapshot_type=get_snapshot_type(snapshot_name,snapshot_description,snapshot_billing_environment)
            ami_exists=False
        volume_exists=check_volume(snapshot['VolumeId'])
        snapshot_age=get_snapshot_age(snapshot['SnapshotId'])
        retention_period=get_retention_period(ami_exists,volume_exists,snapshot_type)
        if snapshot_age > retention_period and not ami_exists:
            try:
                client.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
                #mark_for_deletion=True
            except ClientError as e:
                if 'InvalidSnapshot.InUse' in str(e):
                    print ("skipping this snapshot")
                    continue
        #print(region,snapshot['SnapshotId'],snapshot_name,str(volume_exists),str(ami_exists),str(snapshot_age),snapshot_type,str(retention_period),str(mark_for_deletion)) 
 
