import boto3

def find_passrole_permission_for_all_resources():
    iam_client = boto3.client('iam')

    def check_policy_for_passrole(policy_document, entity_name, entity_type):
        for statement in policy_document.get('Statement', []):
            # Ensure 'Action' and 'Resource' keys are present
            actions = statement.get('Action', [])
            resources = statement.get('Resource', [])

            # Normalize to lists for consistency
            if isinstance(actions, str):
                actions = [actions]
            if isinstance(resources, str):
                resources = [resources]

            # Check if iam:PassRole is in actions and Resource is '*'
            if 'iam:PassRole' in actions and '*' in resources:
                print(f"Found 'iam:PassRole' allowed for all resources in {entity_type} '{entity_name}'")

    # Check inline policies attached to roles
    roles = iam_client.list_roles()['Roles']
    for role in roles:
        role_name = role['RoleName']
        inline_policies = iam_client.list_role_policies(RoleName=role_name)['PolicyNames']
        for policy_name in inline_policies:
            policy_document = iam_client.get_role_policy(RoleName=role_name, PolicyName=policy_name)['PolicyDocument']
            check_policy_for_passrole(policy_document, role_name, 'Role')

    # Check managed policies attached to roles
    for role in roles:
        role_name = role['RoleName']
        attached_policies = iam_client.list_attached_role_policies(RoleName=role_name)['AttachedPolicies']
        for attached_policy in attached_policies:
            policy_arn = attached_policy['PolicyArn']
            policy_version = iam_client.get_policy(PolicyArn=policy_arn)['Policy']['DefaultVersionId']
            policy_document = iam_client.get_policy_version(PolicyArn=policy_arn, VersionId=policy_version)['PolicyVersion']['Document']
            check_policy_for_passrole(policy_document, role_name, 'Role')

    # Check inline policies attached to users
    users = iam_client.list_users()['Users']
    for user in users:
        user_name = user['UserName']
        inline_policies = iam_client.list_user_policies(UserName=user_name)['PolicyNames']
        for policy_name in inline_policies:
            policy_document = iam_client.get_user_policy(UserName=user_name, PolicyName=policy_name)['PolicyDocument']
            check_policy_for_passrole(policy_document, user_name, 'User')

    # Check managed policies attached to users
    for user in users:
        user_name = user['UserName']
        attached_policies = iam_client.list_attached_user_policies(UserName=user_name)['AttachedPolicies']
        for attached_policy in attached_policies:
            policy_arn = attached_policy['PolicyArn']
            policy_version = iam_client.get_policy(PolicyArn=policy_arn)['Policy']['DefaultVersionId']
            policy_document = iam_client.get_policy_version(PolicyArn=policy_arn, VersionId=policy_version)['PolicyVersion']['Document']
            check_policy_for_passrole(policy_document, user_name, 'User')

    # Check inline policies attached to groups
    groups = iam_client.list_groups()['Groups']
    for group in groups:
        group_name = group['GroupName']
        inline_policies = iam_client.list_group_policies(GroupName=group_name)['PolicyNames']
        for policy_name in inline_policies:
            policy_document = iam_client.get_group_policy(GroupName=group_name, PolicyName=policy_name)['PolicyDocument']
            check_policy_for_passrole(policy_document, group_name, 'Group')

    # Check managed policies attached to groups
    for group in groups:
        group_name = group['GroupName']
        attached_policies = iam_client.list_attached_group_policies(GroupName=group_name)['AttachedPolicies']
        for attached_policy in attached_policies:
            policy_arn = attached_policy['PolicyArn']
            policy_version = iam_client.get_policy(PolicyArn=policy_arn)['Policy']['DefaultVersionId']
            policy_document = iam_client.get_policy_version(PolicyArn=policy_arn, VersionId=policy_version)['PolicyVersion']['Document']
            check_policy_for_passrole(policy_document, group_name, 'Group')

if __name__ == "__main__":
    find_passrole_permission_for_all_resources()
