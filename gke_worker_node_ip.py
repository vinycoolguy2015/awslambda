#pip install google-cloud-container google-api-python-client
from google.cloud import container_v1
from googleapiclient import discovery

client = container_v1.ClusterManagerClient()
service = discovery.build('compute', 'v1')

ip=[]

#response = client.get_cluster(project_id,zone,cluster_name)
response = client.get_cluster(name='projects/<project_name>/locations/<zone>/clusters/<cluster_name>')
instance_group_urls=(list(response.instance_group_urls))
for instance_group in instance_group_urls:
    data=instance_group.split('zones')[1].split('/')
    compute_zone=data[1]
    instance_group_manager=data[3]
    request = service.instanceGroups().listInstances(project=project_id, zone=compute_zone, instanceGroup=instance_group_manager)
    response = request.execute()
    for instance_data in response['items']:
        instance_name=instance_data['instance'].split('/')[-1]
        instance_ip = service.instances().get(project=project_id,zone=compute_zone,instance=instance_name).execute()['networkInterfaces'][0]['accessConfigs'][0]['natIP']
        ip.append(instance_ip)

print(ip)
