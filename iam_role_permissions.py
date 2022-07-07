import boto3
import json
import xlsxwriter

iam = boto3.client('iam')
marker = None

workbook = xlsxwriter.Workbook('roles.xlsx')
worksheet = workbook.add_worksheet(name='roles_permissions')
text_format = workbook.add_format({'text_wrap': True,'align':'vcenter'})
heading_format = workbook.add_format({'bold': True, 'font_color': 'red','align':'center'})
row=3

worksheet.write('A1', 'RoleName',heading_format)
worksheet.write('B1', 'AssumeRole',heading_format)
worksheet.write('C1', 'Policy Type',heading_format)
worksheet.write('D1', 'Policy Name',heading_format)
worksheet.write('E1', 'Policy Document',heading_format)

while True:
    paginator = iam.get_paginator('list_roles')
    response_iterator = paginator.paginate( PaginationConfig={'PageSize': 1000,'StartingToken': marker})
    for page in response_iterator:
        role_data=page['Roles']
        for role in role_data:
            gcc_role=False
            role_name=role['RoleName']
            role_tag_data=iam.get_role(RoleName=role_name)
            if 'Tags' in role_tag_data['Role']:
                tags=role_tag_data['Role']['Tags']
                assume_role_policy_doc=role_tag_data['Role']['AssumeRolePolicyDocument']
                for tag in tags:
                    if tag['Key'] == 'Zone':
                        gcc_role=True
                        break
            if gcc_role==True:
                policy_doc=''
                managed_policy_doc=''
                managed_policy=''
                worksheet.write('A'+str(row),role_name)
                worksheet.write('B'+str(row),json.dumps(assume_role_policy_doc))
                get_managed_policies=iam.list_attached_role_policies(RoleName=role_name)
                get_inline_policies=iam.list_role_policies(RoleName=role_name)
                if len(get_managed_policies['AttachedPolicies'] )> 0:
                    for policy in get_managed_policies['AttachedPolicies']:
                        if policy['PolicyName'][0].isupper():
                            worksheet.write('C'+str(row),'AWSManagedPolicy')
                            worksheet.write('D'+str(row),policy['PolicyName'])
                            row=row+1
			else:
                            managed_policy_doc=iam.get_policy(PolicyArn=policy['PolicyArn'])
                            policy_version = iam.get_policy_version(PolicyArn = policy['PolicyArn'], VersionId = managed_policy_doc['Policy']['DefaultVersionId'])
                            managed_policy=policy_version['PolicyVersion']['Document']['Statement']
                            worksheet.write('C'+str(row),'CustomerManagedPolicy')
                            worksheet.write('D'+str(row),policy['PolicyName'])
                            worksheet.write('E'+str(row),json.dumps(managed_policy))
                            row=row+1
		if len(get_inline_policies['PolicyNames']) > 0:
                    for policy in get_inline_policies['PolicyNames']:
                        worksheet.write('C'+str(row),'CustomerManagedPolicy')
                        worksheet.write('D'+str(row),policy)
                        policy_doc = iam.get_role_policy(RoleName=role_name,PolicyName=policy)	
                        worksheet.write('E'+str(row),json.dumps(policy_doc['PolicyDocument']))
                        row=row+1
    try:
         marker = page['Marker']
    except KeyError:
         break
    finally:
         workbook.close()
