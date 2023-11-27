import boto3
client = boto3.client('cloudfront')

response = client.list_distributions()
for distribution in response['DistributionList']['Items']:
        print(distribution['Id'])
        response = client.get_distribution_config(Id=distribution['Id'])
        if response['DistributionConfig']['DefaultCacheBehavior']['LambdaFunctionAssociations']['Quantity']>0:
                for lambda_function in response['DistributionConfig']['DefaultCacheBehavior']['LambdaFunctionAssociations']['Items']:
                        if 'security_headers' in lambda_function['LambdaFunctionARN']:
                                print("Default Cache Behavior is using "+lambda_function['LambdaFunctionARN'])
                        if 'redirect_to_index_html' in lambda_function['LambdaFunctionARN']:
                                print("Default Cache Behavior is using "+lambda_function['LambdaFunctionARN'])
        if 'cache_behavior' in response['DistributionConfig']:
                for cache_behavior in response['DistributionConfig']['CacheBehaviors']['Items']:
                        if cache_behavior['LambdaFunctionAssociations']['Quantity']>0:
                                for lambda_function in cache_behavior['LambdaFunctionAssociations']['Items']:
                                        if 'security_headers' in lambda_function['LambdaFunctionARN']:
                                                print(lambda_function["PathPattern"]+" Cache Behavior is using "+lambda_function['LambdaFunctionARN'])
                                        if 'redirect_to_index_html' in lambda_function['LambdaFunctionARN']:
                                                print(lambda_function["PathPattern"]+"  Cache Behavior is using "+lambda_function['LambdaFunctionARN'])
        print("------")
