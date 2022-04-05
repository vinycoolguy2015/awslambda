import boto3
import json
ecs_client = boto3.client('ecs',region_name='ap-southeast-1')
cw_client = boto3.client('cloudwatch', region_name='ap-southeast-1')
metrics=["CpuUtilized","MemoryUtilized","RunningTaskCount"]
response = ecs_client.list_clusters()
for cluster in response['clusterArns']:
   widgets=[]
   cluster_name=cluster.split('/')[-1]
   services= ecs_client.list_services(cluster=cluster)
   for service in services['serviceArns']:
      service_name=service.split('/')[-1]
      for metric in metrics:
         widgets.append({"type": "metric","width": 6,"height": 6,"properties": {"metrics": [["ECS/ContainerInsights", metric, "ServiceName", service_name, "ClusterName", cluster_name]],
                        "view": "timeSeries",
                        "stacked": False,
                        "region": "ap-southeast-1",
                        "stat": "Average",
                        "period": 60,
                        "title": service_name+"_"+metric
                }
        })
   widget_data=json.dumps(widgets)
   widget_data="{\"widgets\": "+widget_data+"}"
   response = cw_client.put_dashboard(DashboardName=cluster_name+"_metrics", DashboardBody= widget_data)
