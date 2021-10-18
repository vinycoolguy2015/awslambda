import boto3
import time
client = boto3.client('ssm')

# Scan for patches

response=client.send_command(
        InstanceIds=['i-08d4c52a7c56db0bc'],
        DocumentName='AWS-RunPatchBaseline',
        DocumentVersion='$LATEST',
        TimeoutSeconds=900,
        Parameters={
              'Operation': [
                      'Scan'
                        ],
                'RebootOption': [
                        'NoReboot'
                          ]
                },
        OutputS3BucketName='bucket1989',
        OutputKeyPrefix='ssm',
        )
time.sleep(10)

waiter = client.get_waiter('command_executed')
waiter.wait(CommandId=response['Command']['CommandId'],InstanceId='i-08d4c52a7c56db0bc')

# Get Patch State

response = client.describe_instance_patch_states(
    InstanceIds=[
        'i-08d4c52a7c56db0bc',
    ],
    NextToken='string',
    MaxResults=50
)

#Get Patch details

response = client.describe_instance_patches(
    InstanceId='i-08d4c52a7c56db0bc',
    MaxResults=50
)

results = response["Patches"]
while "NextToken" in response:
    response = client.describe_instance_patches(InstanceId='i-08d4c52a7c56db0bc',MaxResults=50,NextToken=response['NextToken'])
    results.extend(response["Patches"])

print("Package status before patching\n"+str(results))

#Create AMI before patching

execution_response=client.start_automation_execution(
DocumentName='ami',
DocumentVersion='$LATEST',
Parameters={
  "InstanceId": [
    "i-08d4c52a7c56db0bc"
  ],
  "NoReboot": [
    "true"
  ],
  "AMINameValue": [
    "Ubuntu"
    ],
  "DeleteOnValue": [
    "19-10-2021"
    ]
  })


# Get AMI creation status
response = client.describe_automation_executions(
    Filters=[
        {
            'Key': 'ExecutionId',
            'Values': [execution_response['AutomationExecutionId']]
        },
    ],
    MaxResults=50,
)
while response['AutomationExecutionMetadataList'][0]['AutomationExecutionStatus'] in ["Pending","InProgress"]:
   print("Image creation in progress")
   time.sleep(10)
   response = client.describe_automation_executions(Filters=[{'Key': 'ExecutionId','Values': [execution_response['AutomationExecutionId']]},],MaxResults=50)
if response['AutomationExecutionMetadataList'][0]['AutomationExecutionStatus'] != "Success":   
   print("Image creation failed")
else:
   print("Image creation completed")


#Patch instance
print("Patching started")
response=client.send_command(
        InstanceIds=['i-08d4c52a7c56db0bc'],
        DocumentName='AWS-RunPatchBaseline',
        DocumentVersion='$LATEST',
        TimeoutSeconds=900,
        Parameters={
              'Operation': [
                      'Install'
                        ],
                'RebootOption': [
                        'RebootIfNeeded'
                          ]
                }
        )
time.sleep(10)

waiter = client.get_waiter('command_executed')
waiter.wait(CommandId=response['Command']['CommandId'],InstanceId='i-08d4c52a7c56db0bc',WaiterConfig={'Delay': 30,'MaxAttempts': 50})

# Post Patching State

response = client.describe_instance_patch_states(
            InstanceIds=[
                        'i-08d4c52a7c56db0bc',
                            ],
                NextToken='string',
                    MaxResults=50
                    )

#Post Patching details

response = client.describe_instance_patches(
            InstanceId='i-08d4c52a7c56db0bc',
                MaxResults=50
                )

results = response["Patches"]
while "NextToken" in response:
        response = client.describe_instance_patches(InstanceId='i-08d4c52a7c56db0bc',MaxResults=50,NextToken=response['NextToken'])
        results.extend(response["Patches"])
print("Post patching package status\n"+str(results))
