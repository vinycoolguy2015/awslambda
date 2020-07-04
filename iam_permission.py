import json
import boto3
import xlsxwriter

iam = boto3.client("iam")
marker = None

workbook = xlsxwriter.Workbook('iam_user_permissions.xlsx')
worksheet = workbook.add_worksheet(name='iam_user_permissions')
text_format = workbook.add_format({'text_wrap': True,'align':'vcenter'})
heading_format = workbook.add_format({'bold': True, 'font_color': 'red','align':'center'})
row=3

worksheet.write('A1', 'UserName',heading_format)
worksheet.write('B1', 'Effect',heading_format)
worksheet.write('C1', 'Action',heading_format)
worksheet.write('D1', 'NotAction',heading_format)
worksheet.write('E1', 'Resource',heading_format)
worksheet.write('F1', 'Condition',heading_format)
worksheet.write('G1', 'Permission Source',heading_format)


def write_data_to_excel(worksheet,user,permission,policytype):
    worksheet.write('A'+str(row),user['UserName'],text_format)
    worksheet.write('B'+str(row),permission['Effect'],text_format)
    if 'Action' in permission:
        if isinstance(permission['Action'], (list)):
            worksheet.write('C'+str(row),'\n'.join(permission['Action']),text_format)
        elif isinstance(permission['Action'].encode('ascii'), (str)):
            worksheet.write('C'+str(row),permission['Action'],text_format)
    elif 'NotAction' in permission:
        if isinstance(permission['NotAction'], (list)):
            worksheet.write('D'+str(row),'\n'.join(permission['NotAction']),text_format)
        elif isinstance(permission['NotAction'].encode('ascii'), (str)):
            worksheet.write('D'+str(row),permission['NotAction'],text_format)
        
                                                
    if isinstance(permission['Resource'], (list)):
        worksheet.write('E'+str(row),'\n'.join(permission['Resource']),text_format)
    elif isinstance(permission['Resource'].encode('ascii'), (str)):
        worksheet.write('E'+str(row),permission['Resource'],text_format)
    
    if 'Condition' in permission:
        worksheet.write('F'+str(row),str(permission['Condition']),text_format)
    else:
        worksheet.write('F'+str(row),'',text_format)
    worksheet.write('G'+str(row),policytype,text_format)

                                   
while True:
    paginator = iam.get_paginator('list_users')
    response_iterator = paginator.paginate( PaginationConfig={'PageSize': 1000,'StartingToken': marker})
    for page in response_iterator:
        u = page['Users']
        for user in u:
            print("Fetching IAM permissions for "+user['UserName'])
            inline_user_policies=iam.list_user_policies(UserName=user['UserName'])
            managed_policies= iam.list_attached_user_policies(UserName=user['UserName'])
            groups=iam.list_groups_for_user(UserName=user['UserName'])
            if len(groups['Groups']) > 0:
                for group in groups['Groups']:
                    group_inline_policies = iam.list_group_policies(GroupName=group['GroupName'])
                    group_managed_policies = iam.list_attached_group_policies(GroupName=group['GroupName'])
                    if len(group_inline_policies['PolicyNames']) > 0:
                        for policy in group_inline_policies['PolicyNames']:
                            group_inline_policiy_detail= iam.get_group_policy(GroupName=group['GroupName'],PolicyName=policy)
                            data=json.dumps(group_inline_policiy_detail['PolicyDocument'])
                            permissions=json.loads(data)['Statement']
                            for permission in permissions:
                                write_data_to_excel(worksheet,user,permission,'Group Inline Policy')
                                row=row+1
                    if len(group_managed_policies['AttachedPolicies']) > 0:
                        for policy in group_managed_policies['AttachedPolicies']:
                            group_managed_policiy_detail= iam.get_policy(PolicyArn=policy['PolicyArn'])
                            policy_version = iam.get_policy_version(PolicyArn = policy['PolicyArn'], VersionId = group_managed_policiy_detail['Policy']['DefaultVersionId'])
                            data=json.dumps(policy_version['PolicyVersion']['Document'])
                            permissions=json.loads(data)['Statement']
                            for permission in permissions:
                                write_data_to_excel(worksheet,user,permission,'Group Managed Policy')
                                row=row+1
                                        
            if len(inline_user_policies['PolicyNames']) > 0:
                for policy in inline_user_policies['PolicyNames']:
                    user_inline_policiy_detail= iam.get_user_policy(UserName=user['UserName'],PolicyName=policy)
                    data=json.dumps(user_inline_policiy_detail['PolicyDocument'])
                    permissions=json.loads(data)['Statement']
                    for permission in permissions:
                        write_data_to_excel(worksheet,user,permission,'User Inline Policy')
                        row=row+1
                        
            if len(managed_policies['AttachedPolicies']) >0:
                for policy in managed_policies['AttachedPolicies']:
                    user_managed_policiy_detail= iam.get_policy(PolicyArn=policy['PolicyArn'])
                    policy_version = iam.get_policy_version(PolicyArn = policy['PolicyArn'], VersionId = user_managed_policiy_detail['Policy']['DefaultVersionId'])
                    data=json.dumps(policy_version['PolicyVersion']['Document'])
                    permissions=json.loads(data)['Statement']
                    for permission in permissions:
                        write_data_to_excel(worksheet,user,permission,'User Managed Policy')
                        row=row+1
                        
                
    try:
        marker = page['Marker']
    except KeyError:
        break
    finally:
        workbook.close()
