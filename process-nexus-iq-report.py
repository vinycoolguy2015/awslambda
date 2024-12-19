import requests
from requests.auth import HTTPBasicAuth
import urllib3

# Suppress the SSL certificate verification warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

base_url="https://nexus-iq.app.com"
application_name='app_application1/' 

#Generate a token
username = "abc"
password = "xyz"


def get_application_id(application_name):
    url = f"{base_url}/api/v2/reports/applications"
    response = requests.get(url, auth=HTTPBasicAuth(username, password), verify=False)
    if response.status_code == 200:
        data = response.json()
    for item in data:
        if application_name in item.get('reportDataUrl', ''):
            application_id = item.get('applicationId')
            break
    print(application_id)
    return application_id

def get_application_report_url(application_id):
    url = f"{base_url}/api/v2/reports/applications/{application_id}"
    response = requests.get(url, auth=HTTPBasicAuth(username, password), verify=False)
    if response.status_code == 200:
        data = response.json()
        report_url=data[0]['reportDataUrl']
    return report_url

def process_application_report(report_url):
    vuln_packages=[]
    url = f"{base_url}/{report_url}"
    response = requests.get(url, auth=HTTPBasicAuth(username, password), verify=False)
    if response.status_code == 200:
        data = response.json()
    components = data.get('components', [])
    for component in components:
        package_name = component.get('displayName', 'Unknown')
        package_url = component.get('packageUrl', 'Unknown')
        security_issues = component.get('securityData', {}).get('securityIssues', [])
        if security_issues:  # Only print packages with vulnerabilities
            vuln_packages.append(package_url)
            print(f"Package: {package_name}")
            print(f"  URL: {package_url}")
            print(f"  Vulnerabilities Found: {len(security_issues)}")
        	
            for issue in security_issues:
                issue_id = issue.get('issueId', 'Unknown')
                severity = issue.get('severity', 'Unknown')
                description = issue.get('description', 'No description available')
                print(f"    - ID: {issue_id}, Severity: {severity}")
                print(f"      Description: {description}")
    return vuln_packages

def get_waiver(application_id):
    waived_packages=[]
    url = f"{base_url}/api/v2/policyWaivers/application/{application_id}"
    response = requests.get(url, auth=HTTPBasicAuth(username, password), verify=False)
    if response.status_code == 200:
        data = response.json()
        for packages in data:
            waived_packages.append(packages['associatedPackageUrl'])
        return waived_packages

        

if __name__ == "__main__":	
    application_id=get_application_id(application_name)
    report_url=get_application_report_url(application_id)
    print(process_application_report(report_url))
    print(get_waiver(application_id))
