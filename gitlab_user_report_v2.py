import requests
import urllib3
import csv

# Replace these with your actual values

GITLAB_BASE_URL = "https://gitlab.com'"
PRIVATE_TOKEN = ""
GROUP1_NAME = "group1"
GROUP2_NAME = "group2"
TOKEN_NAME= "report"

# Access level mapping
access_level_mapping = {
    10: 'Guest',
    20: 'Reporter',
    30: 'Developer',
    40: 'Maintainer',
    50: 'Owner'
}

headers = {"PRIVATE-TOKEN": PRIVATE_TOKEN}


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Function to get PAT ID
def get_pat_id():
    tokens = []
    page = 1
    while True:
        response = requests.get(f'{GITLAB_BASE_URL}/api/v4/personal_access_tokens?page={page}', headers=headers,verify=False)
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

# Function to delete the PAT
def delete_pat(pat_id):
    response = requests.delete(f'{GITLAB_BASE_URL}/api/v4/personal_access_tokens/{pat_id}', headers=headers,verify=False)
    if response.status_code == 204:
        print("Personal Access Token deleted successfully.")
    else:
        print(f"Failed to delete Personal Access Token: {response.status_code} - {response.text}")

def get_group_id(group_name):
    url = f"{GITLAB_BASE_URL}/api/v4/groups?search={group_name}"
    response = requests.get(url, headers=headers,verify=False)

    if response.status_code != 200:
        print(f"Failed to retrieve group ID for '{group_name}': {response.status_code}")
        return None

    groups = response.json()
    for group in groups:
        if group['name'].lower() == group_name.lower():
            return group['id']

    print(f"Group '{group_name}' not found")
    return None

def get_projects_in_group(group_id):
    projects = []
    page = 1
    per_page = 100

    while True:
        url = f"{GITLAB_BASE_URL}/api/v4/groups/{group_id}/projects?page={page}&per_page={per_page}"
        response = requests.get(url, headers=headers,verify=False)

        if response.status_code != 200:
            print(f"Failed to retrieve projects: {response.status_code}")
            return []

        data = response.json()
        if not data:
            break

        projects.extend(data)
        page += 1

    return projects

def get_all_projects_in_group_and_subgroups(group_id):
    all_projects = []

    def fetch_projects(group_id):
        nonlocal all_projects
        projects = get_projects_in_group(group_id)
        all_projects.extend(projects)

        url = f"{GITLAB_BASE_URL}/api/v4/groups/{group_id}/subgroups"
        response = requests.get(url, headers=headers,verify=False)

        if response.status_code != 200:
            print(f"Failed to retrieve subgroups: {response.status_code}")
            return

        subgroups = response.json()
        for subgroup in subgroups:
            fetch_projects(subgroup['id'])

    fetch_projects(group_id)
    return all_projects

def list_users_and_access_levels(project_id):
    users = []
    page = 1
    per_page = 100

    while True:
        url = f"{GITLAB_BASE_URL}/api/v4/projects/{project_id}/members/all?page={page}&per_page={per_page}"
        response = requests.get(url, headers=headers,verify=False)

        if response.status_code != 200:
            print(f"Failed to retrieve users for project ID {project_id}: {response.status_code}")
            return []

        data = response.json()
        if not data:
            break

        users.extend(data)
        page += 1

    return users

def main():
    with open('project_users_access.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Group Name','Project Name', 'Username', 'Access Level','User Creation Date','User Status'])

        for group_name in [GROUP1_NAME,GROUP2_NAME]:
            group_id = get_group_id(group_name)
            if not group_id:
                continue

            all_projects = get_all_projects_in_group_and_subgroups(group_id)
            for project in all_projects:
                users = list_users_and_access_levels(project['id'])
                for user in users:
                    if user['access_level'] != 20:  # Exclude Reporters
                        access_level = access_level_mapping.get(user['access_level'], 'Unknown')
                        writer.writerow([group_name,project['name'], user['username'], access_level,user['created_at'],user['state']])

if __name__ == "__main__":
    main()
    # Delete the PAT at the end
    delete_pat(get_pat_id())
