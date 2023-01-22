import boto3
import os
import json
def lambda_handler(event, context):
	codedeploy_client = boto3.client('codedeploy')
	lambda_client = boto3.client('lambda')

	deploymentId = event['DeploymentId']
	lifecycleEventHookExecutionId = event['LifecycleEventHookExecutionId']
	functionToTest = os.environ['NewVersion']
	lambdaResult=""
	try:
		response = lambda_client.invoke(FunctionName=functionToTest,InvocationType='RequestResponse')
		result = json.loads(response.get('Payload').read())
		if result['body'] == '16':
			lambdaResult = "Succeeded"
		else:
			lambdaResult = "Failed"
	except Exception as e:
		print(e)
		lambdaResult = "Failed"
	finally:
		response = codedeploy_client.put_lifecycle_event_hook_execution_status(deploymentId=deploymentId,lifecycleEventHookExecutionId=lifecycleEventHookExecutionId,status=lambdaResult)


