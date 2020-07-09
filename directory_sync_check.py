import boto3 
import time
import os
from datetime import datetime

ssm_client = boto3.client('ssm')
ec2_client = boto3.client('ec2')
ses_client=boto3.client('ses')
s3_client=boto3.client('s3')

def send_email(subject,body):
    ses_client.send_email(Source=os.environ['Source'],Destination={'ToAddresses': [os.environ['Recipient']]},
    Message={
        'Subject': {
            'Data': subject
        },
        'Body': {
            'Text': {
                'Data': body
            }
        }
    }
)

def copy_python_script(instanceid):
    response = ssm_client.send_command(
            InstanceIds=[instanceid],
            DocumentName="AWS-RunShellScript",
            Parameters={'commands': ["""cat <<EOF > /tmp/files.py
import os
import glob
path=glob.glob("/opt/dir*")
files = []
for dir in path:
    for root,d_names,f_names in os.walk(dir):
        for f in f_names:
            if f.lower().endswith('.txt'):
                files.append(os.path.join(root, f))
print(','.join(files))

    """
            ],"executionTimeout":["30"]}, TimeoutSeconds=30)
    return response['Command']['CommandId']

def run_python_script(instanceid):
    response=ssm_client.send_command( InstanceIds=[ instanceid ], DocumentName='AWS-RunShellScript', Comment='Run a remote python script', Parameters={ "commands":["python /tmp/files.py"],"executionTimeout":["90"] },TimeoutSeconds=30,OutputS3BucketName=os.environ['s3_bucket'])
    return response['Command']['CommandId']

def check_copy_python_script_status(commandid,instanceid):
    status='Failed'
    while True:
        output = ssm_client.get_command_invocation(CommandId=commandid,InstanceId=instanceid)
        if output['StatusDetails'] in ['InProgress','Pending']:
            time.sleep(5)
        elif output['StatusDetails'] =='Success':
            status='Success'
            break
        else:
            break
    return status
    
    
def run_python_script_status(instanceid,commandid):
    files=set()
    output_file=''
    while True:
        output = ssm_client.get_command_invocation(CommandId=commandid,InstanceId=instanceid)
        if output['StatusDetails'] in ['InProgress','Pending']:
            time.sleep(5)
        elif output['StatusDetails'] =='Success':
            output_file=commandid+'/'+instanceid+'/awsrunShellScript/0.awsrunShellScript/stdout'
            #files.update(output['StandardOutputContent'].split(','))
            s3_client.download_file(os.environ['s3_bucket'], output_file,'/tmp/'+instanceid)
            text_file = open("/tmp/"+instanceid, "r")
            lines = text_file.read().split(',')
            files.update(lines)
            s3 = boto3.resource('s3')
            bucket = s3.Bucket(os.environ['s3_bucket'])
            bucket.objects.filter(Prefix=commandid+"/").delete()
            break
        else:
            break
    return files
    
def check_status():
    update_status=False
    time_difference=0
    try:
        results = s3_client.head_object(Bucket=os.environ['s3_bucket'], Key=os.environ['test_file'])
        file_timestamp=results['LastModified']
        time_difference=datetime.utcnow()-file_timestamp.replace(tzinfo=None)
        if time_difference.total_seconds() > int(os.environ['wait_time']):
            s3_client.put_object(Bucket=os.environ['s3_bucket'],Key=os.environ['test_file'])
            update_status=True
    except:
        s3_client.put_object(Bucket=os.environ['s3_bucket'],Key=os.environ['test_file'])
        update_status=True
    return update_status
            
            
    

def lambda_handler(event, context):
    
    if not check_status():
        print("Servers are still not in Sync.")
        return
    
    instance1=ec2_client.describe_instances(Filters=[{'Name': 'tag:Name','Values': [os.environ['Instance1']]}])['Reservations'][0]['Instances'][0]['InstanceId']
    instance2=ec2_client.describe_instances(Filters=[{'Name': 'tag:Name','Values': [os.environ['Instance2']]}])['Reservations'][0]['Instances'][0]['InstanceId']
    
    
    command_id=copy_python_script(instance1)
    time.sleep(5) # To avoid InvocationDoesNotExist error
    server1_copy_script_status=check_copy_python_script_status(command_id,instance1)
    if server1_copy_script_status == 'Failed':
        send_email(os.environ['Subject'],"Problem copying script on "+os.environ['Instance1']+".Please check if SSM agent is running on the server.")
        return
    
    command_id=copy_python_script(instance2)
    time.sleep(5) # To avoid InvocationDoesNotExist error
    server2_copy_script_status=check_copy_python_script_status(command_id,instance2)
    if server2_copy_script_status == 'Failed':
        send_email(os.environ['Subject'],"Problem copying script on "+os.environ['Instance2']+".Please check if SSM agent is running on the server.")
        return
    
    command_id = run_python_script(instance1)
    time.sleep(5) # To avoid InvocationDoesNotExist error
    server1_files=run_python_script_status(instance1,command_id)
    
    command_id = run_python_script(instance2)
    time.sleep(5) # To avoid InvocationDoesNotExist error
    server2_files=run_python_script_status(instance2,command_id)
    
        
    if not server1_files:
        send_email(os.environ['Subject'],"Problem copying script on "+os.environ['Instance1']+".Please check if SSM agent is running on the server.")
        return
    if not server2_files:
        send_email(os.environ['Subject'],"Problem copying script on "+os.environ['Instance2']+".Please check if SSM agent is running on the server.")
        return
   
    
    server2_missingFiles=server1_files.difference(server2_files)
    server1_missingFiles=server2_files.difference(server1_files)
    
    if not server1_missingFiles and not server2_missingFiles:
        print("Servers are in sync")
        s3_client.delete_object(Bucket=os.environ['s3_bucket'],Key=os.environ['test_file'])
        #send_email(os.environ['Subject'],"Servers are in sync")
    else:
        if server1_missingFiles and server2_missingFiles:
            send_email(os.environ['Subject'],os.environ["Instance1"] + " and "+os.environ["Instance2"]+ " are not in sync.\n\n\nFiles missing on "+os.environ['Instance1']+' :\n '+','.join(list(server1_missingFiles))+"\n\n\nFiles missing on "+os.environ['Instance2']+':\n '+'.'.join(list(server2_missingFiles)))
        elif server1_missingFiles and not server2_missingFiles:
            send_email(os.environ['Subject'],os.environ["Instance1"] + " and "+os.environ["Instance2"]+ " are not in sync.\n\n\nFiles missing on "+os.environ['Instance1']+' :\n '+','.join(list(server1_missingFiles)))
        elif server2_missingFiles and not server1_missingFiles:
            send_email(os.environ['Subject'],os.environ["Instance1"] + " and "+os.environ["Instance2"]+ " are not in sync.\n\n\nFiles missing on "+os.environ['Instance2']+':\n '+'.'.join(list(server2_missingFiles)))
    
        
    
	    
    
    
    
    
    
    
    
