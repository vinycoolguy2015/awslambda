from pymongo import MongoClient
import time
import boto3

MONGO_DB='admin'

cloudwatch = boto3.client('cloudwatch', region_name='ap-south-1')
    
connection = MongoClient('mongodb://vinayak:Mongo1086#@server1.example.com:27017,server2.example.com:27017,server3.example.com:27017/?replicaSet=example-replica-set') 

db = connection[MONGO_DB]

replicaset_status=db.command("replSetGetStatus")
server_status=db.command("serverStatus")
  

#Server Stats
member_count=len(replicaset_status['members'])

server1_stats=next(item for item in replicaset_status['members'] if item["name"] == "server1.example.com:27017")
server1_health=server1_stats['health']
server1_state=server1_stats['state']
server1_uptime=server1_stats['uptime']

server2_stats=next(item for item in replicaset_status['members'] if item["name"] == "server2.example.com:27017")
server2_health=server2_stats['health']
server2_state=server2_stats['state']
server2_uptime=server2_stats['uptime']

server3_stats=next(item for item in replicaset_status['members'] if item["name"] == "server3.example.com:27017")
server3_health=server3_stats['health']
server3_state=server3_stats['state']
server3_uptime=server3_stats['uptime']

#Connection Stats
current_connections=server_status['connections']['current']
available_connections=server_status['connections']['available']

#Memory Stats
resident_memory=server_status['mem']['resident']
virtual_memory=server_status['mem']['virtual']

#Network Stats
network_in=server_status['network']['bytesIn']
network_out=server_status['network']['bytesOut']

#I/O Stats
read_io=server_status['wiredTiger']['connection']['total read I/Os']
write_io=server_status['wiredTiger']['connection']['total write I/Os']
open_file=server_status['wiredTiger']['connection']['files currently open']

#Queue Stats
read_request_queued=server_status['globalLock']['currentQueue']['readers']
write_request_queued=server_status['globalLock']['currentQueue']['writers']
page_faults=server_status['extra_info']['page_faults']

#Reader Stats
active_readers=server_status['globalLock']['activeClients']['readers']
active_writers=server_status['globalLock']['activeClients']['writers']

#Push metric
timestamp=int(time.time())

server_metrics_name=['active_writers','active_writers','page_faults','write_request_queued','read_request_queued','read_io','write_io','open_file','network_in','network_out','resident_memory','virtual_memory','current_connections','available_connections']

server_metrics=[]
for metric in server_metrics_name:
  data={}
  data['MetricName']=metric
  data['Timestamp']=timestamp
  data['Value']=vars()[metric]
  data['Unit']='Count'
  server_metrics.append(data)

  
replicaset_metrics_name=['member_count','server1_health','server1_state','server1_uptime','server2_health','server2_state','server2_uptime','server3_health','server3_state','server3_uptime']
replicaset_metrics=[]
for metric in replicaset_metrics_name:
  data={}
  data['MetricName']=metric
  data['Timestamp']=timestamp
  data['Value']=vars()[metric]
  data['Unit']='Count'
  replicaset_metrics.append(data)

response = cloudwatch.put_metric_data(Namespace='mongo',MetricData=server_metrics)
response = cloudwatch.put_metric_data(Namespace='mongo',MetricData=replicaset_metrics)
