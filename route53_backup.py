import boto3

zone_id=''
client = boto3.client('route53')
paginator = client.get_paginator('list_resource_record_sets')

try:
    source_zone_records = paginator.paginate(HostedZoneId=zone_id)
    for record_set in source_zone_records:
        for record in record_set['ResourceRecordSets']:
            if record['Type'] in ['A','CNAME']:
                if 'AliasTarget' in record:
                    print (record['Name']+','+record['Type']+','+record['AliasTarget']['DNSName'])
                else:
                    records=[]
                    for ip in record['ResourceRecords']:
                        records.append(ip['Value'])
                    print (record['Name']+','+record['Type']+','+','.join(records))
except Exception as error:
	print(record)
	print ('An error occured getting source zone records '+ str(error))
	exit(1)
