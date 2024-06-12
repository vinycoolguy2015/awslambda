import boto3

def list_lambda_functions_with_provisioned_concurrency():
    lambda_client = boto3.client('lambda',region_name='ap-southeast-1')
    
    # List all Lambda functions
    response = lambda_client.list_functions()
    
    provisioned_concurrency_functions = []
    
    # Iterate through the functions and check if provisioned concurrency is configured
    for function in response['Functions']:
        function_name = function['FunctionName']
        
        # List aliases for the function
        aliases = lambda_client.list_aliases(FunctionName=function_name)['Aliases']
        for alias in aliases:
            alias_name = alias['Name']
            
            # Check if provisioned concurrency is configured for the alias
            try:
                provisioned_concurrency_response = lambda_client.get_provisioned_concurrency_config(
                    FunctionName=function_name,
                    Qualifier=alias_name
                )
                provisioned_concurrency = provisioned_concurrency_response['RequestedProvisionedConcurrentExecutions']
                
                provisioned_concurrency_functions.append({
                    'FunctionName': function_name,
                    'Qualifier': alias_name,
                    'ProvisionedConcurrency': provisioned_concurrency
                })
            except lambda_client.exceptions.ProvisionedConcurrencyConfigNotFoundException:
                # Provisioned concurrency not configured for this alias
                pass
        
        # List versions for the function
        versions = lambda_client.list_versions_by_function(FunctionName=function_name)['Versions']
        for version in versions:
            version_number = version['Version']
            
            # Skip the $LATEST version
            if version_number == '$LATEST':
                continue
            
            # Check if provisioned concurrency is configured for the version
            try:
                provisioned_concurrency_response = lambda_client.get_provisioned_concurrency_config(
                    FunctionName=function_name,
                    Qualifier=version_number
                )
                provisioned_concurrency = provisioned_concurrency_response['RequestedProvisionedConcurrentExecutions']
                
                provisioned_concurrency_functions.append({
                    'FunctionName': function_name,
                    'Qualifier': version_number,
                    'ProvisionedConcurrency': provisioned_concurrency
                })
            except lambda_client.exceptions.ProvisionedConcurrencyConfigNotFoundException:
                # Provisioned concurrency not configured for this version
                pass
    
    return provisioned_concurrency_functions

# Usage example
provisioned_concurrency_functions = list_lambda_functions_with_provisioned_concurrency()

# Print the list of functions with provisioned concurrency
for function in provisioned_concurrency_functions:
    print(f"Function Name: {function['FunctionName']}, Qualifier: {function['Qualifier']}, Provisioned Concurrency: {function['ProvisionedConcurrency']}")
