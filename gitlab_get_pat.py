import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Replace with your GitLab instance URL and your personal access token
GITLAB_URL = 'https://gitlab.com'
ACCESS_TOKEN = '<PROVIDE_TOKEN_VALUE>'
TOKEN_NAME='test'

# Headers for the API requests
headers = {
    'Private-Token': ACCESS_TOKEN
}

# Function to list all PATs (requires admin permissions)
def list_personal_access_tokens():
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
    return tokens

# List all PATs and print their details
tokens = list_personal_access_tokens()
for token in tokens:
    if token['active']==True and token['name']==TOKEN_NAME:
    	print(f"ID: {token['id']}, Name: {token['name']}, Created At: {token['created_at']}, Expires At: {token['expires_at']}")

