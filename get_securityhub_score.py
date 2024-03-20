import sys
import boto3
import json

def get_standards_status(clientSh, accountId):
    filters = {'AwsAccountId': [{'Value': accountId, 'Comparison': 'EQUALS'}],
               'ProductName': [{'Value': 'Security Hub', 'Comparison': 'EQUALS'}],
               'RecordState': [{'Value': 'ACTIVE', 'Comparison': 'EQUALS'}]}

    pages = clientSh.get_paginator('get_findings').paginate(Filters=filters, MaxResults=100)
    standardsDict = {}

    for page in pages:
        for finding in page['Findings']:
            standardsDict = build_standards_dict(finding, standardsDict)
    return standardsDict

def build_standards_dict(finding, standardsDict):
    if any(x in json.dumps(finding) for x in ['Compliance', 'ProductFields']):
        if 'Compliance' in finding:
            status = finding['Compliance']['Status']
            prodField = finding['ProductFields']
            if (finding['RecordState'] == 'ACTIVE' and finding['Workflow']['Status'] != 'SUPPRESSED'):  # ignore disabled controls and suppressed findings
                control = None
                # get values, json differnt for controls...
                if 'StandardsArn' in prodField:  # for aws fun
                    control = prodField['StandardsArn']
                    rule = prodField['ControlId']
                elif 'StandardsGuideArn' in prodField:  # for cis fun
                    control = prodField['StandardsGuideArn']
                    rule = prodField['RuleId']
                #ignore custom findings
                if control is not None:
                    controlName = control.split('/')[1]  # get readable name from arn
                    if controlName not in standardsDict:
                        standardsDict[controlName] = {rule: status} # add new in
                    elif not (rule in standardsDict[controlName] and (status == 'PASSED')):  # no need to update if passed
                        standardsDict[controlName][rule] = status
    return standardsDict

def generateScore(standardsDict):
    resultDict = {}
    for control in standardsDict:
        passCheck = 0
        totalControls = len(standardsDict[control])
        passCheck = len({test for test in standardsDict[control] if standardsDict[control][test] == 'PASSED'})

        # generate score
        score = round(passCheck/totalControls * 100)  # generate score
        resultDict[control] = {"Score": score} #build dictionary
    return resultDict

def main():

    accountId = boto3.client('sts').get_caller_identity().get('Account') # get current account id

    # create boto securityhub client
    client = (boto3.session.Session(region_name='ap-southeast-1')).client('securityhub')

    scores = generateScore(get_standards_status(client, accountId))
    print(scores)

if __name__ == '__main__':
    main()
