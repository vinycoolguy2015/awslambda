import boto3

def lambda_handler(event, context):
    client = boto3.client('codepipeline',region_name='us-west-1')
    response = client.get_pipeline(name='beanstalk')
    new_version=response['pipeline']['version']+1
    for data in response['pipeline']['stages']:
        if data['name'] == 'Deploy':
            deployment_environment=data['actions'][0]['configuration']['EnvironmentName']
       
            if deployment_environment == 'development-environment':
                new_deployment_environment = 'production-environment'
            elif deployment_environment == 'production-environment':
                new_deployment_environment = 'development-environment'
            
            break
    try:
        response = client.update_pipeline(
            pipeline={
                'name': 'beanstalk',
                'roleArn': 'arn:aws:iam::8086:role/service-role/AWSCodePipelineServiceRole-us-west-1-beanstalk',
                'artifactStore': {
                    'type': 'S3',
                    'location': 'codepipeline-us-west-1-632590770179'
                    },
                    "stages": [
                    {
                        "name": "Source",
                        "actions": [
                        {
                            "name": "Source",
                            "actionTypeId": {
                                "category": "Source",
                                "owner": "AWS",
                                "provider": "CodeCommit",
                                "version": "1"
                            },
                            "runOrder": 1,
                            "configuration": {
                                "BranchName": "main",
                                "OutputArtifactFormat": "CODE_ZIP",
                                "PollForSourceChanges": "false",
                                "RepositoryName": "beanstalk"
                            },
                            "outputArtifacts": [
                                {
                                    "name": "SourceArtifact"
                                }
                            ],
                            "inputArtifacts": [],
                            "region": "us-west-1",
                            "namespace": "SourceVariables"
                        }
                    ]
                },
                {
                    "name": "Deploy",
                    "actions": [
                        {
                            "name": "Deploy",
                            "actionTypeId": {
                                "category": "Deploy",
                                "owner": "AWS",
                                "provider": "ElasticBeanstalk",
                                "version": "1"
                            },
                            "runOrder": 1,
                            "configuration": {
                                "ApplicationName": "HelloWorld",
                                "EnvironmentName": new_deployment_environment
                            },
                            "outputArtifacts": [],
                            "inputArtifacts": [
                                {
                                    "name": "SourceArtifact"
                                }
                            ],
                            "region": "us-west-1",
                            "namespace": "DeployVariables"
                        }
                    ]
                },
                {
                    "name": "Env-URL-Swap",
                    "actions": [
                        {
                            "name": "Env-URL-Swap",
                            "actionTypeId": {
                                "category": "Invoke",
                                "owner": "AWS",
                                "provider": "Lambda",
                                "version": "1"
                            },
                            "runOrder": 1,
                            "configuration": {
                                "FunctionName": "beanstalk_env_swap"
                            },
                            "outputArtifacts": [],
                            "inputArtifacts": [
                                {
                                    "name": "SourceArtifact"
                                }
                            ],
                            "region": "us-west-1"
                        }
                    ]
                },
                {
                    "name": "Update-BeansTalk-Deployment-Environment",
                    "actions": [
                        {
                            "name": "Update-BeansTalk-Deployment-Environment",
                            "actionTypeId": {
                                "category": "Invoke",
                                "owner": "AWS",
                                "provider": "Lambda",
                                "version": "1"
                            },
                            "runOrder": 1,
                            "configuration": {
                                "FunctionName": "update_beanstalk_pipeline"
                            },
                            "outputArtifacts": [],
                            "inputArtifacts": [
                                {
                                    "name": "SourceArtifact"
                                }
                            ],
                            "region": "us-west-1"
                        }
                    ]
                }
            ],
            'version': new_version
            }
        )
        client.put_job_success_result(jobId=event['CodePipeline.job']['id'])
    except Exception as e:
        print(e)
        client.put_job_failure_result(jobId=event['CodePipeline.job']['id'],failureDetails={'type': 'JobFailed','message': 'CNAME swapping failed','externalExecutionId': context.aws_request_id})
    


