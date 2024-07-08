import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Replace with your GitLab instance URL and your personal access token
GITLAB_URL = 'https://gitlab.com'
ACCESS_TOKEN = '<PROVIDE_TOKEN_VALUE_WITH_API_ACCESS>'
TOKEN_NAME = '<PROVIDE_TOKEN_NAME_WITH_API_ACCESS>'

# Headers for the API requests
headers = {
    'Private-Token': ACCESS_TOKEN
}

# Access level mapping
access_level_mapping = {
    10: 'Guest',
    20: 'Reporter',
    30: 'Developer',
    40: 'Maintainer',
    50: 'Owner'
}

#Function to get PAT ID
def get_pat_id():
    tokens = []
    page = 1
    while True:
        response = requests.get(f'{GITLAB_URL}/api/v4/personal_access_tokens?page={page}', headers=headers,verify=False)
        if response.status_code != 200:
            break
        data = response.json()
        if not data:
            break
        tokens.extend(data)
        page += 1
    for token in tokens:
    	if token['active']==True and token['name']==TOKEN_NAME:
    		return token['id']

# Function to get all groups
def get_all_groups():
    groups = []
    page = 1
    while True:
        response = requests.get(f'{GITLAB_URL}/api/v4/groups?page={page}', headers=headers,verify=False)
        if response.status_code != 200:
            break
        data = response.json()
        if not data:
            break
        groups.extend(data)
        page += 1
    return groups

# Function to get all projects in a group
def get_projects_in_group(group_id):
    projects = []
    page = 1
    while True:
        response = requests.get(f'{GITLAB_URL}/api/v4/groups/{group_id}/projects?page={page}', headers=headers,verify=False)
        if response.status_code != 200:
            break
        data = response.json()
        if not data:
            break
        projects.extend(data)
        page += 1
    return projects

# Function to get all users in a project with their access levels
def get_users_in_project(project_id):
    users = []
    page = 1
    while True:
        response = requests.get(f'{GITLAB_URL}/api/v4/projects/{project_id}/members/all?page={page}', headers=headers,verify=False)
        if response.status_code != 200:
            break
        data = response.json()
        if not data:
            break
        users.extend(data)
        page += 1
    return users

# Function to get all users in a group with their access levels
def get_users_in_group(group_id):
    users = []
    page = 1
    while True:
        response = requests.get(f'{GITLAB_URL}/api/v4/groups/{group_id}/members/all?page={page}', headers=headers,verify=False)
        if response.status_code != 200:
            break
        data = response.json()
        if not data:
            break
        users.extend(data)
        page += 1
    return users

# Main script to get all users in all projects and groups with their access levels
all_users = {}

# Get all groups
groups = get_all_groups()

# Get users in each group
for group in groups:
    group_users = get_users_in_group(group['id'])
    for user in group_users:
        all_users[user['username']] = {
            'name': user['name'],
            'group_access_level': access_level_mapping.get(user['access_level'], 'Unknown')
        }

    # Get all projects in the group
    projects = get_projects_in_group(group['id'])
    for project in projects:
        project_users = get_users_in_project(project['id'])
        for user in project_users:
            if user['username'] in all_users:
                all_users[user['username']]['project_access_level'] = access_level_mapping.get(user['access_level'], 'Unknown')
            else:
                all_users[user['username']] = {
                    'name': user['name'],
                    'project_access_level': access_level_mapping.get(user['access_level'], 'Unknown')
                }

# Print all users with their access levels
print("All users in all projects and groups with their access levels:")
for username, details in all_users.items():
    print(f"Username: {username}, Name: {details['name']}, Group Access Level: {details.get('group_access_level', 'N/A')}, Project Access Level: {details.get('project_access_level', 'N/A')}")

# Function to delete the PAT
def delete_pat(pat_id):
    response = requests.delete(f'{GITLAB_URL}/api/v4/personal_access_tokens/{pat_id}', headers=headers,verify=False)
    if response.status_code == 204:
        print("Personal Access Token deleted successfully.")
    else:
        print(f"Failed to delete Personal Access Token: {response.status_code} - {response.text}")

# Delete the PAT at the end
delete_pat(get_pat_id())
