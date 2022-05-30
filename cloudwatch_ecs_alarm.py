import boto3
import json

ecs_client = boto3.client('ecs',region_name='ap-southeast-1')
cw_client = boto3.client('cloudwatch', region_name='ap-southeast-1')

sns='arn:aws:sns:ap-southeast-1:35571622:sns_topic'
metrics=["CpuUtilized","MemoryUtilized","RunningTaskCount"]
threshold = {'delayed': {'MemoryUtilized': 100, 'CpuUtilized': 20,'RunningTaskCount':2},
          'passenger': {'MemoryUtilized': 80, 'CpuUtilized': 10, 'RunningTaskCount': 2},
          'apache': {'MemoryUtilized': 50, 'CpuUtilized': 5, 'RunningTaskCount': 3}
          }

response = ecs_client.list_clusters()
for cluster in response['clusterArns']:
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
        cw_client.put_metric_alarm(AlarmName="%s_%s" % (service_name,metric),ComparisonOperator='GreaterThanThreshold',EvaluationPeriods=1,MetricName=metric,Namespace='ECS/ContainerInsights',Period=300,Statistic='Average',Threshold=threshold[threshold_data][metric],AlarmDescription="Alarm when %s %s exceeds threshold!" % (service_name,metric),Dimensions=[{'Name': 'ServiceName','Value': service_name},{'Name':'ClusterName','Value':cluster_name}],Unit='None',ActionsEnabled=True,AlarmActions=[sns])
