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

# Function to get all backup rules for a given BackupPlanId
def get_all_backup_rule_details(backup_plan_id):
    try:
        response = backup_client.get_backup_plan(BackupPlanId=backup_plan_id)
        rules = response['BackupPlan']['Rules']
        rule_details = [(rule['RuleName'], rule['ScheduleExpression']) for rule in rules]
        return rule_details
    except Exception as e:
        print(f"Error retrieving Backup Rules for ID {backup_plan_id}: {e}")
    return []

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

# Function to get Resource Type from Resource ARN
def get_resource_type(resource_arn):
    # The resource type is typically the second-to-last component of the ARN
    # Example: arn:aws:dynamodb:ap-southeast-1:123456789012:table/MyTable
    try:
        return resource_arn.split(':')[2]  # Return the service name (e.g., dynamodb)
    except IndexError:
        return "Unknown"

# Prepare CSV output
output_file = 'latest_recovery_points.csv'

# Write to CSV
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)

    # Get all backup vaults
    vault_names = get_backup_vaults()

    # Initialize a header row
    csv_headers = ["ResourceArn", "ResourceType", "LatestRecoveryPoint", "CreationDate", "BackupPlanId", "BackupPlanName"]
    
    # Initialize a dict to store all rules for header generation
    rule_names = set()
    
    # First pass to collect all recovery points and rule names
    all_data = []

    for vault_name in vault_names:
        latest_recovery_points = get_latest_recovery_points(vault_name)

        for resource_arn, recovery_point in latest_recovery_points.items():
            backup_plan_id = recovery_point.get('CreatedBy', {}).get('BackupPlanId', None)

            if backup_plan_id is not None:
                backup_plan_name = get_backup_plan_name(backup_plan_id)  # Get the backup plan name
                backup_rules = get_all_backup_rule_details(backup_plan_id)  # Get all rule names and schedules
                resource_type = get_resource_type(resource_arn)  # Get resource type
                
                # Collect rule names for dynamic header generation
                for rule_name, rule_schedule in backup_rules:
                    rule_names.add(rule_name)

                all_data.append([
                    resource_arn,
                    resource_type,
                    recovery_point['RecoveryPointArn'],
                    recovery_point['CreationDate'],
                    backup_plan_id,
                    backup_plan_name,
                    backup_rules  # Store all backup rules for this resource
                ])

    # Generate dynamic CSV headers for rules
    for rule_name in rule_names:
        csv_headers.append(f"{rule_name} Schedule")

    # Write headers
    writer.writerow(csv_headers)

    # Second pass to write data, including rules in columns
    for data in all_data:
        resource_rules = {rule[0]: rule[1] for rule in get_all_backup_rule_details(data[4])}  # Get rules for each resource
        row = data[:6]  # Base row without rules

        # Append schedule for each rule as columns
        for rule_name in rule_names:
            row.append(resource_rules.get(rule_name, "N/A"))  # Use "N/A" if the rule is not found

        writer.writerow(row)

print(f"Latest recovery points with BackupPlanId written to {output_file}.")

