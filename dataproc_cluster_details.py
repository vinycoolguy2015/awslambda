#add google-cloud-dataproc==0.5.0 in requirements

import base64
import json
from google.cloud import dataproc_v1
from google.cloud.dataproc_v1.gapic.transports import cluster_controller_grpc_transport
from googleapiclient.discovery import build


project_id='playground-s-11-b2c3df'
firewall = 'test2'
region='us-central1'
zone='us-central1-c'
ip=[]
cluster_name='cluster-ec21'
network='global/networks/test'

compute = build('compute', 'v1')
cluster_transport = cluster_controller_grpc_transport.ClusterControllerGrpcTransport(address='us-central1-dataproc.googleapis.com:443')
dataproc_cluster_client = dataproc_v1.ClusterControllerClient(cluster_transport)

cluster = dataproc_cluster_client.get_cluster(project_id, region,cluster_name)
master_nodes=list(cluster.config.master_config.instance_names)
worker_nodes=list(cluster.config.worker_config.instance_names)

result = compute.instances().list(project=project_id, zone=zone).execute()
for instance in result["items"]:
    if instance['name'] in master_nodes or instance['name'] in worker_nodes:
        ip.append(instance['networkInterfaces'][0]['accessConfigs'][0]['natIP'])

firewall_body = {'sourceRanges': ip,'allowed':[{'IPProtocol': 'tcp','ports': ['22']}],'network':network}
request = compute.firewalls().update(project=project_id, firewall=firewall, body=firewall_body)
response = request.execute()
