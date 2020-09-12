#Create a pub/sub sink with this query
#resource.type="cloud_dataproc_cluster"
#protoPayload.methodName="google.cloud.dataproc.v1.ClusterController.CreateCluster"

#in requirements.txt add
#google-cloud-dataproc==0.5.0

import base64
import json
from google.cloud import dataproc_v1
from google.cloud.dataproc_v1.gapic.transports import cluster_controller_grpc_transport

def hello_pubsub(event, context):
    cluster_transport = cluster_controller_grpc_transport.ClusterControllerGrpcTransport(address='us-central1-dataproc.googleapis.com:443')
    dataproc_cluster_client = dataproc_v1.ClusterControllerClient(cluster_transport)
    project_id=''
    region='us-central1'
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    data=json.loads(pubsub_message)
    cluster_name=data['resource']['labels']['cluster_name']
    print(cluster_name+" dataproc cluster created")
    #for cluster in dataproc_cluster_client.list_clusters(project_id, region):
        #if cluster.cluster_name == cluster_name:
            #print(cluster)
    
   
