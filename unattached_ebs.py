import boto3
import os

REGIONS = [
    'us-east-1',
    'eu-west-1',
    'ap-northeast-1'
]

sns = boto3.client('sns')


def lambda_handler(event, context):
    sns_topic_arn = os.environ['REPORT_SNS_TOPIC']
    account_id = context.invoked_function_arn.split(":")[4]

    report = []
    for region in REGIONS:
        client = boto3.client('ec2', region_name=region)

        paginator = client.get_paginator('describe_volumes')
        response_iterator = paginator.paginate(
            Filters=[
                {
                    'Name': 'status',
                    'Values': [
                        'available',
                    ]
                },
            ]
        )

        for response in response_iterator:
            for vol in response['Volumes']:
                report_line = "{} - {} ({}GB)".format(vol['VolumeId'], vol['AvailabilityZone'], vol['Size'])
                if 'Tags' in vol:
                    report_line = report_line + " with tags: "
                    for tag in vol['Tags']:
                        report_line = report_line + " {}: {},".format(tag['Key'], tag['Value'])

                report.append(report_line)

    if len(report) > 0:
        print(report)
        sns.publish(
            TopicArn=sns_topic_arn,
            Subject="List of Unattached EBS volumes",
            Message="The following unattached EBS volumes have been found in account {}:\n\n".format(account_id) + "\n".join(report)
        )
