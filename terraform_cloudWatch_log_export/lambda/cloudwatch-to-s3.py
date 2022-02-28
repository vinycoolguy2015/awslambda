import boto3
import os
from pprint import pprint
import time
from datetime import datetime

logs = boto3.client('logs')
ssm = boto3.client('ssm')

def lambda_handler(event, context):
    extra_args = {}
    log_groups = []
    log_groups_to_export = []
    
    if 'S3_BUCKET' not in os.environ:
        print("Error: S3_BUCKET not defined")
        return
    
    print("--> S3_BUCKET=%s" % os.environ["S3_BUCKET"])
    
    while True:
        response = logs.describe_log_groups(**extra_args)
        log_groups = log_groups + response['logGroups']
        
        if not 'nextToken' in response:
            break
        extra_args['nextToken'] = response['nextToken']
    
    for log_group in log_groups:
        response = logs.list_tags_log_group(logGroupName=log_group['logGroupName'])
        log_group_tags = response['tags']
        if 'ExportToS3' in log_group_tags and log_group_tags['ExportToS3'] == 'true':
            log_groups_to_export.append(log_group['logGroupName'])
    
    for log_group_name in log_groups_to_export:
        ssm_parameter_name = ("/log-exporter-last-export/%s" % log_group_name).replace("//", "/")
        try:
            ssm_response = ssm.get_parameter(Name=ssm_parameter_name)
            ssm_value = ssm_response['Parameter']['Value']
        except ssm.exceptions.ParameterNotFound:
            ssm_value = "0"
        
        export_to_time = int(round(time.time() * 1000))
        current_date=datetime.today().strftime('%Y-%m-%d')
        
        print("--> Exporting %s to %s" % (log_group_name, os.environ['S3_BUCKET']))
        
        if export_to_time - int(ssm_value) < (24 * 60 * 60 * 1000):
            # Haven't been 24hrs from the last export of this log group
            print("    Skipped until 24hrs from last export is completed")
            continue
        
        max_retries = 10
        while max_retries > 0:
            try:
                response = logs.create_export_task(
                    logGroupName=log_group_name,
                    fromTime=int(ssm_value),
                    to=export_to_time,
                    destination=os.environ['S3_BUCKET'],
                    destinationPrefix=log_group_name.strip('/') + '/' + current_date
                )
                print("    Task created: %s" % response['taskId'])
                ssm_response = ssm.put_parameter(
                    Name=ssm_parameter_name,
                    Type="String",
                    Value=str(export_to_time),
                    Overwrite=True)

                break
                
            except logs.exceptions.LimitExceededException:
                max_retries = max_retries - 1
                print("    Need to wait until all tasks are finished (LimitExceededException). Continuing %s additional times" % (max_retries))
                time.sleep(5)
                continue
            
            except Exception as e:
                print("    Error exporting %s: %s" % (log_group_name, getattr(e, 'message', repr(e))))
                break
