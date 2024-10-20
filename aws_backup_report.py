import boto3
import csv

# Initialize the Backup client
backup_client = boto3.client('backup')

# Function to get all backup vaults
def get_backup_vaults():
    vaults = []
    response = backup_client.list_backup_vaults()
    
    # Keep paginating if there are more vaults
    while True:
        vaults.extend(response['BackupVaultList'])
        if 'NextToken' in response:
            response = backup_client.list_backup_vaults(NextToken=response['NextToken'])
        else:
            break
    return [vault['BackupVaultName'] for vault in vaults]

# Function to get the backup plan name from BackupPlanId
def get_backup_plan_name(backup_plan_id):
    try:
        response = backup_client.get_backup_plan(BackupPlanId=backup_plan_id)
        return response['BackupPlan']['BackupPlanName']
    except Exception as e:
        print(f"Error retrieving Backup Plan Name for ID {backup_plan_id}: {e}")
        return "Unknown"

# Function to get backup rules for a given BackupPlanId
def get_backup_rule_details(backup_plan_id):
    try:
        response = backup_client.get_backup_plan(BackupPlanId=backup_plan_id)
        rules = response['BackupPlan']['Rules']
        # Assuming you want to return the first rule's name and schedule
        if rules:
            return rules[0]['RuleName'], rules[0]['ScheduleExpression']
    except Exception as e:
        print(f"Error retrieving Backup Rules for ID {backup_plan_id}: {e}")
    return "Unknown", "Unknown"

# Function to get latest recovery points for a given vault
def get_latest_recovery_points(vault_name):
    response = backup_client.list_recovery_points_by_backup_vault(BackupVaultName=vault_name)
    latest_recovery_points = {}

    # Process recovery points
    for recovery_point in response['RecoveryPoints']:
        resource_arn = recovery_point['ResourceArn']
        creation_date = recovery_point['CreationDate']
        
        # Get BackupPlanId and BackupRuleId, if available
        backup_plan_id = recovery_point.get('CreatedBy', {}).get('BackupPlanId', None)
        backup_rule_id = recovery_point.get('CreatedBy', {}).get('BackupRuleId', None)

        # If the resource is already in the dictionary, compare the creation dates
        if resource_arn in latest_recovery_points:
            existing_point = latest_recovery_points[resource_arn]
            # Compare creation dates
            if creation_date > existing_point['CreationDate']:
                latest_recovery_points[resource_arn] = recovery_point
        else:
            # Add the recovery point if it's not already recorded
            latest_recovery_points[resource_arn] = recovery_point

    return latest_recovery_points

# Prepare CSV output
output_file = 'latest_recovery_points.csv'
csv_headers = ["ResourceArn", "LatestRecoveryPoint", "CreationDate", "BackupPlanId", "BackupPlanName", "BackupRuleId", "BackupRuleName", "BackupRuleSchedule"]

# Write to CSV
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(csv_headers)  # Write headers

    # Get all backup vaults
    vault_names = get_backup_vaults()

    # Loop through each vault to get latest recovery points
    for vault_name in vault_names:
        latest_recovery_points = get_latest_recovery_points(vault_name)

        # Write the data rows to CSV only if BackupPlanId is present
        for resource_arn, recovery_point in latest_recovery_points.items():
            backup_plan_id = recovery_point.get('CreatedBy', {}).get('BackupPlanId', None)
            backup_rule_id = recovery_point.get('CreatedBy', {}).get('BackupRuleId', None)

            # Only write to CSV if BackupPlanId is not None
            if backup_plan_id is not None:
                backup_plan_name = get_backup_plan_name(backup_plan_id)  # Get the backup plan name
                backup_rule_name, backup_rule_schedule = get_backup_rule_details(backup_plan_id)  # Get the rule name and schedule
                writer.writerow([
                    resource_arn,
                    recovery_point['RecoveryPointArn'],
                    recovery_point['CreationDate'],
                    backup_plan_id,
                    backup_plan_name,  # Include the Backup Plan Name
                    backup_rule_id if backup_rule_id is not None else 'N/A',
                    backup_rule_name,  # Include the Backup Rule Name
                    backup_rule_schedule  # Include the Backup Rule Schedule
                ])

print(f"Latest recovery points with BackupPlanId written to {output_file}.")

