import boto3
import json
import os

ecs_client = boto3.client('ecs',region_name='ap-southeast-1')
cw_client = boto3.client('cloudwatch', region_name='ap-southeast-1')

metrics=["CpuUtilized","MemoryUtilized","RunningTaskCount"]
sns=os.environ['sns_topic']
threshold = {'delayed': {'MemoryUtilized': os.environ['delayed_memory_utilized'], 'CpuUtilized': os.environ['delayed_cpu_utilized'],'RunningTaskCount':os.environ['delayed_task_count']},
 'passenger': {'MemoryUtilized': os.environ['passenger_memory_utilized'], 'CpuUtilized': os.environ['passenger_cpu_utilized'],'RunningTaskCount':os.environ['passenger_task_count']},
 'apache': {'MemoryUtilized': os.environ['apache_memory_utilized'], 'CpuUtilized': os.environ['apache_cpu_utilized'],'RunningTaskCount':os.environ['apache_task_count']}
}

unit={"CpuUtilized":"None","MemoryUtilized":"Megabytes","RunningTaskCount":"Count"}

def lambda_handler(event, context):
   response = ecs_client.list_clusters()
   for cluster in response['clusterArns']:
      widgets=[]
      cluster_name=cluster.split('/')[-1]
      services= ecs_client.list_services(cluster=cluster)
      for service in services['serviceArns']:
         threshold_data=''
         service_name=service.split('/')[-1]
         for key in threshold:
            if service_name.find(key) > -1:
               threshold_data=key
               break
         if threshold_data=='':
            continue
         for metric in metrics:
            widgets.append({"type": "metric","width": 6,"height": 6,"properties": {"metrics": [["ECS/ContainerInsights", metric, "ServiceName", service_name, "ClusterName", cluster_name]],"view": "timeSeries","stacked": False,"region": "ap-southeast-1","stat": "Average","period": 60,"title": service_name+"_"+metric}})
            cw_client.put_metric_alarm(AlarmName="%s_%s" % (service_name,metric),ComparisonOperator='GreaterThanThreshold',EvaluationPeriods=1,MetricName=metric,Namespace='ECS/ContainerInsights',Period=300,Statistic='Average',Threshold=int(threshold[threshold_data][metric]),AlarmDescription="Alarm when %s %s exceeds threshold!" % (service_name,metric),Dimensions=[{'Name': 'ServiceName','Value': service_name},{'Name':'ClusterName','Value':cluster_name}],Unit=unit[metric],ActionsEnabled=True,AlarmActions=[sns])
      widget_data=json.dumps(widgets)
      widget_data="{\"widgets\": "+widget_data+"}"
      response = cw_client.put_dashboard(DashboardName=cluster_name+"_metrics", DashboardBody= widget_data)

