#!/usr/bin/python
import requests, json,sys
from datadog import initialize, api
from time import time

output_file="instance_utilization.csv"

api_key= ''
application_key= ''

url = "https://app.datadoghq.com/reports/v2/overview?api_key="+api_key+"&application_key="+application_key
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

r = requests.get(url,headers=headers)

if r.status_code == 200:
    result= r.json()
    instance_data={}
    for data in result['rows']:
        if 'aws_id' in data and 'host_name' in data:
            instance_data[data['aws_id']]=data['host_name']

            
options = {
'api_key': '',
'app_key': ''
}

hosts=['i-0decf5fb9ebfd270e']

initialize(**options)

end = int(time())
start = end - (3600*24*30)

csv_file = open(output_file,'w+')
csv_file.write("Instance ID,Hostname,Minimum Avaialble CPU(%),Total Memory(MB),Minimum Usable Memory Available(MB)\n\n")

for host in hosts:
    if host in instance_data.keys():
        hostname=instance_data[host]
        
        #Fetch toal memory on a server
        query='min:system.mem.total{host:'+hostname+'}'
        results = api.Metric.query(start=start, end=end, query=query)
        if not "Rate limit of 300 requests in 3600 seconds reached" in str(results):
            if len(results['series']) > 0:
                total_available_memory=(min(results['series'][0]['pointlist'], key=lambda x: x[1])[1])/(1024*1024)
            else:
                total_available_memory="Total Memory metrics for "+host+" is not available"
        else:
            print("Rate limit of 300 requests in 3600 seconds reached")
            sys.exit(1)
        
        #Fetch minimum usable memory on a server
        query='min:system.mem.usable{host:'+hostname+'}'
        results = api.Metric.query(start=start, end=end, query=query)
        if not "Rate limit of 300 requests in 3600 seconds reached" in str(results):
            if len(results['series']) > 0:
                minimum_memory_free=(min(results['series'][0]['pointlist'], key=lambda x: x[1])[1])/(1024*1024)
            else:
                minimum_memory_free="Memory metrics for "+host+" is not available"
        else:
            print("Rate limit of 300 requests in 3600 seconds reached")
            sys.exit(1)
        
        #Fetch minimum available CPU on a server
        query='min:system.cpu.idle{host:'+hostname+'}'
        results = api.Metric.query(start=start, end=end, query=query)
        if not "Rate limit of 300 requests in 3600 seconds reached" in str(results):
            if len(results['series']) > 0:
                minimum_cpu_free=(min(results['series'][0]['pointlist'], key=lambda x: x[1]))[1]
            else:
                minimum_cpu_free="CPU metrics for "+host+" is not available"
        else:
            print("Rate limit of 300 requests in 3600 seconds reached")
            sys.exit(1)
        csv_file.write("%s,%s,%s,%s,%s\n" %(host,hostname,minimum_cpu_free,total_available_memory,minimum_memory_free))
        csv_file.flush()
    else:
        print("Hostname for "+host+" is not available")
        
    

	
