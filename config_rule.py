import boto3

def lambda_handler(event, context):
    
    ACCOUNT_ID = boto3.client('sts').get_caller_identity()['Account']
    CONFIG_CLIENT = boto3.client('config')
    MY_RULE = "restricted-ssh"
    
    EC2_CLIENT = boto3.client('ec2')

    non_compliant_detail = CONFIG_CLIENT.get_compliance_details_by_config_rule(ConfigRuleName=MY_RULE, ComplianceTypes=['NON_COMPLIANT'],Limit=100)
    results=non_compliant_detail['EvaluationResults']
    if len(results) > 0:
        print('The following resource(s) are not compliant with AWS Config rule: '+ MY_RULE)
        for security_group in results:
            security_group_id=security_group['EvaluationResultIdentifier']['EvaluationResultQualifier']['ResourceId']
            response = EC2_CLIENT.describe_security_groups( GroupIds=[security_group_id])
            for sg in response['SecurityGroups']:
                for ip in sg['IpPermissions']:
                    if 'FromPort' in ip and ip['FromPort']==22:
                        for cidr in ip['IpRanges']:
                            if cidr['CidrIp']=='0.0.0.0/0':
                                print("Revoking public access to SSH port for security group "+security_group_id)
                                EC2_CLIENT.revoke_security_group_ingress(GroupId=security_group_id, IpPermissions=[ip])
                                
                                
