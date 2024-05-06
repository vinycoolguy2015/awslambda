import boto3
import os
from pprint import pprint
import time
from datetime import datetime

logs = boto3.client('logs',region_name='us-east-1')


extra_args = {}
log_groups = []
log_groups_to_export = []
    
while True:
    response = logs.describe_log_groups(**extra_args)
    log_groups = log_groups + response['logGroups']
    if not 'nextToken' in response:
        break
    extra_args['nextToken'] = response['nextToken']


for log_group in log_groups:
	log_groups_to_export.append(log_group['logGroupName'])

for log_group_name in log_groups_to_export:
	export_to_time = int(round(time.time() * 1000))
	current_date=datetime.today().strftime('%Y-%m-%d')
	print("--> Exporting %s" % (log_group_name))

	max_retries = 10
	while max_retries > 0:
		try:
			response = logs.create_export_task(logGroupName=log_group_name,fromTime=1701360000000,to=export_to_time,destination='s3-log-bucket',destinationPrefix='us-east-1/'+log_group_name.strip('/') + '/' + current_date)
			print("Task created: %s" % response['taskId'])
			taskID=response['taskId']
			break
		except logs.exceptions.LimitExceededException:
            max_retries = max_retries - 1
            print("Need to wait until all tasks are finished (LimitExceededException). Continuing %s additional times" % (max_retries))
            time.sleep(5)
            continue
		except Exception as e:
			print("Error exporting %s: %s" % (log_group_name, getattr(e, 'message', repr(e))))
			break
	while True:
		time.sleep(10)
		get_task_status = logs.describe_export_tasks(taskId=taskID)
		task_status=get_task_status['exportTasks'][0]['status']['code']
		if task_status=='COMPLETED':
			print(log_group_name+ " exported successfully")
			break
		elif task_status=='FAILED':
			print(log_group_name+ " exported successfully")
			break
		else: 
			print(taskID+ "status is "+task_status)
