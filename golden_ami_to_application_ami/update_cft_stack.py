from datetime import date
import boto3
import os
import time

def lambda_handler(event, context):
    todays_date = date.today()
    version='.'.join([str(todays_date.year),str(todays_date.month),str(todays_date.day)])
    golden_ami_id=event['golden_ami_id']
    cfclient = boto3.client('cloudformation')
    try:
        response = cfclient.update_stack(StackName=os.environ['STACK_NAME'],UsePreviousTemplate=True,Parameters=[{'ParameterKey': 'ParentImage','ParameterValue': golden_ami_id,},{'ParameterKey': 'Version','ParameterValue': version,}],Capabilities=['CAPABILITY_IAM'])
    except:
        return {"Stack_Status": "Failed"}
        
    while True:
        time.sleep(10)
        stack_detail = cfclient.describe_stacks(StackName=os.environ['STACK_NAME'])
        stack_update_status=stack_detail['Stacks'][0]['StackStatus']
        print('stack_update_status')
        if stack_update_status=='UPDATE_COMPLETE':
            return {"Stack_Status": "Updated"}
            break
        elif stack_update_status in ['UPDATE_FAILED','UPDATE_ROLLBACK_IN_PROGRESS','UPDATE_ROLLBACK_COMPLETE', 'UPDATE_ROLLBACK_FAILED']:
            return {"Stack_Status": "Failed"}
            break




