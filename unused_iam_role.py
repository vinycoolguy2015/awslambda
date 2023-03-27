# https://medium.com/@iknowdevops/how-to-list-unused-iam-roles-in-aws-131d2b99b042
import boto3
import datetime
from datetime import timezone

# Define the IAM client
iam = boto3.client('iam')
current_date = datetime.datetime.now((timezone.utc))
 
# Define the time delta for 60 days
delta = datetime.timedelta(days=60)

# Calculate the date 60 days ago
sixty_days_ago = current_date - delta

# Create a list to store the unused roles
unused_roles = []

# Paginate through the IAM roles and check if they have been used
paginator = iam.get_paginator('list_roles')
for response in paginator.paginate():
    roles = response['Roles']
    for role in roles:
        role_name = role['RoleName']
        last_used = iam.get_role(RoleName=role_name)['Role']['RoleLastUsed']
        if not last_used:
            # The role has never been used
            create_date = role['CreateDate']
            if create_date < sixty_days_ago:
                unused_roles.append(role_name)
        else:
            # The role has been used at least once
            last_used_date = last_used['LastUsedDate']
            if last_used_date < sixty_days_ago:
                unused_roles.append(role_name)

print(unused_roles)
