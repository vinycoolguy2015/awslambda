import boto3

shield_client = boto3.client('shield',region_name='us-east-1')
shield_cw_client = boto3.client('cloudwatch', region_name='us-east-1')
cw_client = boto3.client('cloudwatch', region_name='ap-southeast-1')
nf_client = boto3.client('network-firewall',region_name='ap-southeast-1')
ec2_client = boto3.client('ec2',region_name='ap-southeast-1')
rds_client = boto3.client('rds',region_name='ap-southeast-1')

shield_sns='arn:aws:sns:us-east-1:xxxx:alert-notification'
nf_rds_sns='arn:aws:sns:ap-southeast-1:xxxx:alert-notification'

stateful_nf_metrics=["DroppedPackets","RejectedPackets"]
stateless_nf_metrics=["DroppedPackets","InvalidDroppedPackets","OtherDroppedPackets"]

rds_reader_metrics=[{'Name':'CPUUtilization','Thereshold':80,'Unit':'Percent','ComparisonOperator':'GreaterThanThreshold'},
{'Name':'EBSIOBalance%','Thereshold':20,'Unit':'Percent','ComparisonOperator':'LessThanThreshold'},
{'Name':'ACUUtilization','Thereshold':80,'Unit':'Percent','ComparisonOperator':'GreaterThanThreshold'},
{'Name':'AuroraReplicaLag','Thereshold':50,'Unit':'Milliseconds','ComparisonOperator':'GreaterThanThreshold'},
{'Name':'Deadlocks','Thereshold':1,'Unit':'Count/Second','ComparisonOperator':'GreaterThanThreshold'},
{'Name':'ReadLatency','Thereshold':.01,'Unit':'Seconds','ComparisonOperator':'GreaterThanThreshold'},
{'Name':'CommitLatency','Thereshold':5,'Unit':'Milliseconds','ComparisonOperator':'GreaterThanThreshold'},
{'Name':'FreeableMemory','Thereshold':100000000,'Unit':'Bytes','ComparisonOperator':'LessThanThreshold'},
{'Name':'DiskQueueDepth','Thereshold':5,'Unit':'Count','ComparisonOperator':'GreaterThanThreshold'}
]

rds_writer_metrics=[{'Name':'CPUUtilization','Thereshold':80,'Unit':'Percent','ComparisonOperator':'GreaterThanThreshold'},
{'Name':'EBSIOBalance%','Thereshold':20,'Unit':'Percent','ComparisonOperator':'LessThanThreshold'},
{'Name':'ACUUtilization','Thereshold':80,'Unit':'Percent','ComparisonOperator':'GreaterThanThreshold'},
{'Name':'AuroraReplicaLagMaximum','Thereshold':50,'Unit':'Milliseconds','ComparisonOperator':'GreaterThanThreshold'},
{'Name':'Deadlocks','Thereshold':1,'Unit':'Count/Second','ComparisonOperator':'GreaterThanThreshold'},
{'Name':'WriteLatency','Thereshold':.01,'Unit':'Seconds','ComparisonOperator':'GreaterThanThreshold'},
{'Name':'ReadLatency','Thereshold':.01,'Unit':'Seconds','ComparisonOperator':'GreaterThanThreshold'},
{'Name':'CommitLatency','Thereshold':5,'Unit':'Milliseconds','ComparisonOperator':'GreaterThanThreshold'},
{'Name':'FreeableMemory','Thereshold':10000000000,'Unit':'Bytes','ComparisonOperator':'LessThanThreshold'},
{'Name':'DiskQueueDepth','Thereshold':5,'Unit':'Count','ComparisonOperator':'GreaterThanThreshold'}
]



#Create Shield Alarm
print("Creating Shield Alarms")
response = shield_client.list_protections()
for data in response['Protections']:
  shield_cw_client.put_metric_alarm(AlarmName="%s-%s" % (data['ResourceArn'].split("/")[-1],"Shield-DDoS-Detection"),ComparisonOperator='GreaterThanThreshold',EvaluationPeriods=1,MetricName="DDoSDetected",Namespace='AWS/DDoSProtection',Period=300,Statistic='Maximum',Threshold=0,AlarmDescription="Alarm when DDoS attack is detected by Shield!" ,Dimensions=[{'Name': 'ResourceArn','Value':data['ResourceArn']}],Unit='None',ActionsEnabled=True,AlarmActions=[shield_sns],TreatMissingData="notBreaching")
print("Shield Alarms Created")

#Create Network FireWall Alarm
print("Creating Network Firewall Alarms")
response = nf_client.list_firewalls()
for data in response['Firewalls']:
  
  response = nf_client.describe_firewall(FirewallName=data['FirewallName'])
  for subnet in response['Firewall']['SubnetMappings']:
    response = ec2_client.describe_subnets(
    SubnetIds=[
        subnet['SubnetId']])
    
    for metric in stateful_nf_metrics:
      cw_client.put_metric_alarm(AlarmName="%s-%s-%s" % (data['FirewallName'],"stateful",metric),ComparisonOperator='GreaterThanThreshold',EvaluationPeriods=1,MetricName=metric,Namespace='AWS/NetworkFirewall',Period=300,Statistic='Average',Threshold=100,AlarmDescription="Alarm when Packets Dropped By Network Firewall!" ,Dimensions=[{'Name': 'FirewallName','Value':data['FirewallName']},{'Name':'AvailabilityZone','Value':response['Subnets'][0]['AvailabilityZone']},{'Name':'Engine','Value':'Stateful'}],Unit='None',ActionsEnabled=True,AlarmActions=[nf_rds_sns],TreatMissingData="notBreaching")
    for metric in stateless_nf_metrics:
      cw_client.put_metric_alarm(AlarmName="%s-%s-%s" % (data['FirewallName'],"stateless",metric),ComparisonOperator='GreaterThanThreshold',EvaluationPeriods=1,MetricName=metric,Namespace='AWS/NetworkFirewall',Period=300,Statistic='Average',Threshold=100,AlarmDescription="Alarm when Packets Dropped By Network Firewall!" ,Dimensions=[{'Name': 'FirewallName','Value':data['FirewallName']},{'Name':'AvailabilityZone','Value':response['Subnets'][0]['AvailabilityZone']},{'Name':'Engine','Value':'Stateless'}],Unit='Count',ActionsEnabled=True,AlarmActions=[nf_rds_sns],TreatMissingData="notBreaching")
 
print("Network Firewall Alarms Created")   
#Create RDS Alarm
print("Creating RDS Alarms")
response = rds_client.describe_db_clusters()
for db in response['DBClusters']:
  for metric in rds_reader_metrics:
    cw_client.put_metric_alarm(AlarmName="%s-%s-%s" % (db['DBClusterIdentifier'],"reader",metric['Name']),ComparisonOperator=metric['ComparisonOperator'],EvaluationPeriods=1,MetricName=metric['Name'],Namespace='AWS/RDS',Period=300,Statistic='Average',Threshold=metric['Thereshold'],AlarmDescription="Alarm when metric[Name] goes past metric['Thereshold']!" ,Dimensions=[{'Name': 'Role','Value':'READER'},{'Name':'DBClusterIdentifier','Value':db['DBClusterIdentifier']}],Unit=metric['Unit'],ActionsEnabled=True,AlarmActions=[nf_rds_sns],TreatMissingData="notBreaching")
  for metric in rds_writer_metrics:
    cw_client.put_metric_alarm(AlarmName="%s-%s-%s" % (db['DBClusterIdentifier'],"reader",metric['Name']),ComparisonOperator=metric['ComparisonOperator'],EvaluationPeriods=1,MetricName=metric['Name'],Namespace='AWS/RDS',Period=300,Statistic='Average',Threshold=metric['Thereshold'],AlarmDescription="Alarm when metric[Name] goes past metric['Thereshold']!" ,Dimensions=[{'Name': 'Role','Value':'WRITER'},{'Name':'DBClusterIdentifier','Value':db['DBClusterIdentifier']}],Unit=metric['Unit'],ActionsEnabled=True,AlarmActions=[nf_rds_sns],TreatMissingData="notBreaching")
print("RDS Alarms Created") 


  
