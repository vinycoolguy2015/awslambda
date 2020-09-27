import boto3
import json

client = boto3.client('pricing',aws_access_key_id="",
                        aws_secret_access_key="")  

response = client.get_products(
    ServiceCode='AmazonEC2',
    Filters=[
        {
            'Type': 'TERM_MATCH',
            'Field': 'instanceType',
            'Value': 't3.small'
        },
		{
            'Type': 'TERM_MATCH',
            'Field': 'operatingSystem',
            'Value': 'Linux'
        },
		{
            'Type': 'TERM_MATCH',
            'Field': 'location',
            'Value': 'US East (N. Virginia)' # 'EU (Ireland)'
        },
    ]
)
						
data=json.loads(response['PriceList'][0])['terms']['OnDemand']
id1 = list(data)[0]
id2 = list(data[id1]['priceDimensions'])[0]
print(data[id1]['priceDimensions'][id2]['pricePerUnit']['USD'])
