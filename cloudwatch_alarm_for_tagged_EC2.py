import boto3
import json
import os

AWS_REGION = "ap-southeast-1"
EC2_RESOURCE = boto3.resource('ec2', region_name=AWS_REGION)
cw_client = boto3.client('cloudwatch', region_name=AWS_REGION)
INSTANCE_NAME_TAG_VALUE = ['*Dev*','*dev*']

sns=os.environ['sns_topic']
threshold ={"mem_used_percent":os.environ['mem_used_percent'],"CPUUtilization":os.environ['CPUUtilization'],"disk_used_percent":os.environ['disk_used_percent']}

def lambda_handler(event, context):
   instances = EC2_RESOURCE.instances.filter(Filters=[{'Name': 'tag:Name','Values': INSTANCE_NAME_TAG_VALUE},{'Name': 'instance-state-name','Values': ['running']}])
   tags=set()
   for instance in instances:
      for tag in instance.tags:
         if tag['Key'] == 'Environment':
            tags.add(tag['Value'])
   for environment in tags:
      widgets=[]
      instances = EC2_RESOURCE.instances.filter(
      Filters=[{'Name': 'tag:Environment','Values': [environment]},{'Name': 'instance-state-name','Values': ['running']}])
      for instance in instances:
         for tag in instance.tags:
            if tag['Key'] == 'Name':
               instance_name=tag['Value']
               continue
      
         widgets.append({"type": "metric","width": 6,"height": 6,"properties": {"metrics": [["CWAgent", "mem_used_percent", "InstanceId", instance.id]],"view": "timeSeries","stacked": False,"region": "ap-southeast-1","stat": "Average","period": 60,"title": instance_name+"_mem_used_percent"}})

         widgets.append({"type": "metric","width": 6,"height": 6,"properties": {"metrics": [["AWS/EC2", "CPUUtilization", "InstanceId", instance.id]],"view": "timeSeries","stacked": False,"region": "ap-southeast-1","stat": "Average","period": 60,"title": instance_name+"_CPUUtilization"}})
         
         widgets.append({"type": "metric","width": 6,"height": 6,"properties": {"metrics": [["CWAgent", "disk_used_percent", "path","/","InstanceId", instance.id,"device", "nvme0n1p1", "fstype", "xfs"]],"view": "timeSeries","stacked": False,"region": "ap-southeast-1","stat": "Average","period": 60,"title": instance_name+"_disk_used_percent"}})
         
         
         cw_client.put_metric_alarm(AlarmName="%s_%s" % (instance_name,"mem_used_percent"),ComparisonOperator='GreaterThanThreshold',EvaluationPeriods=1,MetricName="mem_used_percent",Namespace='CWAgent',Period=300,Statistic='Average',Threshold=int(threshold["mem_used_percent"]),AlarmDescription="Alarm when %s %s exceeds threshold!" % (instance_name,"mem_used_percent"),Dimensions=[{'Name': 'InstanceId','Value': instance.id}],Unit='Percent',ActionsEnabled=True,AlarmActions=[sns])
         
         cw_client.put_metric_alarm(AlarmName="%s_%s" % (instance_name,"CPUUtilization"),ComparisonOperator='GreaterThanThreshold',EvaluationPeriods=1,MetricName="CPUUtilization",Namespace='AWS/EC2',Period=300,Statistic='Average',Threshold=int(threshold['CPUUtilization']),AlarmDescription="Alarm when %s %s exceeds threshold!" % (instance_name,"CPUUtilization"),Dimensions=[{'Name': 'InstanceId','Value': instance.id}],Unit='Percent',ActionsEnabled=True,AlarmActions=[sns])
         
         cw_client.put_metric_alarm(AlarmName="%s_%s" % (instance_name,"disk_used_percent"),ComparisonOperator='GreaterThanThreshold',EvaluationPeriods=1,MetricName="disk_used_percent",Namespace='CWAgent',Period=300,Statistic='Average',Threshold=int(threshold["disk_used_percent"]),AlarmDescription="Alarm when %s %s exceeds threshold!" % (instance_name,"disk_used_percent"),Dimensions=[{'Name': 'path','Value': "/"},{'Name': 'InstanceId','Value': instance.id},{'Name': 'device','Value': "nvme0n1p1"},{'Name': 'fstype','Value': 'xfs'}],Unit='Percent',ActionsEnabled=True,AlarmActions=[sns])

      widget_data=json.dumps(widgets)
      widget_data="{\"widgets\": "+widget_data+"}"
      response = cw_client.put_dashboard(DashboardName="WebServer_"+environment+"_metrics", DashboardBody= widget_data)
