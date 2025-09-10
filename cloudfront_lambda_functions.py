import boto3

# Define your list of Lambda function names directly here
lambda_names = [
	'lambda-edge_redirect_to_index_html',
	'maintenance-redirect',
	'lambda-error-redirect',
	'lambda-security_headers'
]
cf_client = boto3.client("cloudfront")

# Get all CloudFront distributions
distributions = []
paginator = cf_client.get_paginator("list_distributions")
for page in paginator.paginate():
    distributions.extend(page.get("DistributionList", {}).get("Items", []))

# Track which Lambdas are found
lambda_usage = {name: [] for name in lambda_names}

# Search through distributions
for dist in distributions:
    dist_id = dist["Id"]
    config = cf_client.get_distribution_config(Id=dist_id)
    dist_config = config["DistributionConfig"]

    # Process DefaultCacheBehavior
    default_behavior = dist_config.get("DefaultCacheBehavior", {})
    lfa = default_behavior.get("LambdaFunctionAssociations", {})
    for assoc in lfa.get("Items", []):
        arn = assoc["LambdaFunctionARN"]
        event_type = assoc.get("EventType", "unknown")
        for name in lambda_names:
            if name in arn:
                version = arn.split(":")[-1]
                lambda_usage[name].append((dist_id, version, event_type, "DefaultCacheBehavior"))

    # Process CacheBehaviors
    for behavior in dist_config.get("CacheBehaviors", {}).get("Items", []):
        path_pattern = behavior.get("PathPattern", "unknown")
        lfa = behavior.get("LambdaFunctionAssociations", {})
        for assoc in lfa.get("Items", []):
            arn = assoc["LambdaFunctionARN"]
            event_type = assoc.get("EventType", "unknown")
            for name in lambda_names:
                if name in arn:
                    version = arn.split(":")[-1]
                    lambda_usage[name].append((dist_id, version, event_type, f"CacheBehavior: {path_pattern}"))

# Print results
for name, usages in lambda_usage.items():
    if usages:
        for dist_id, version, event_type, behavior in usages:
            print(f"✅ Lambda '{name}' is used in CloudFront Distribution '{dist_id}' "
                  f"(Behavior: {behavior}, Event: {event_type}, Version: {version})")
    else:
        print(f"❌ Lambda '{name}' is NOT used in any CloudFront Distribution.")
