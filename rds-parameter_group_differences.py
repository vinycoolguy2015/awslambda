import boto3

def get_parameters(client, param_group_name):
    """Fetch all parameters for a given RDS cluster parameter group"""
    #paginator = client.get_paginator('describe_db_cluster_parameters') #For cluster parameter group
    paginator = client.get_paginator('describe_db_parameters') #For instance parameter group
    params = {}
    #for page in paginator.paginate(DBClusterParameterGroupName=param_group_name): #For cluster parameter group
    for page in paginator.paginate(DBParameterGroupName=param_group_name): # For instance parameter group
        for param in page['Parameters']:
            # Only compare parameters that have a name and a value
            if 'ParameterName' in param:
                params[param['ParameterName']] = {
                    "Value": param.get("ParameterValue"),
                    "ApplyType": param.get("ApplyType"),
                    "IsModifiable": param.get("IsModifiable"),
                    "ApplyMethod": param.get("ApplyMethod"),
                }
    return params

def compare_parameters(params1, params2):
    """Compare two parameter sets and print differences"""
    all_keys = set(params1.keys()).union(set(params2.keys()))
    differences = []
    
    for key in sorted(all_keys):
        p1 = params1.get(key)
        p2 = params2.get(key)
        if p1 != p2:
            differences.append({
                "ParameterName": key,
                "Group1": p1,
                "Group2": p2
            })
    return differences

if __name__ == "__main__":
    # ---- Change these to your parameter group names ----
    group1 = "A"
    group2 = "B"

    client = boto3.client("rds")

    params1 = get_parameters(client, group1)
    params2 = get_parameters(client, group2)

    diffs = compare_parameters(params1, params2)

    if not diffs:
        print("No differences found between the two parameter groups.")
    else:
        print(f"Found {len(diffs)} differences:\n")
        for diff in diffs:
            print(f"Parameter: {diff['ParameterName']}")
            print(f"  {group1}: {diff['Group1']}")
            print(f"  {group2}: {diff['Group2']}")
            print("-" * 60)

