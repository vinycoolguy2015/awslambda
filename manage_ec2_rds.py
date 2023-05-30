import json
import boto3


ec2_client = boto3.client('ec2',region_name='us-east-1')
rds_client = boto3.client('rds',region_name='us-east-1')

def lambda_handler(event, context):
    instances = []
    
    if event:
        if "instance_type" not in event or event['instance_type'] not in ["ec2","rds"]:
            print("Instance type not provided or incorrect instance type provided. "+event['instance_type'])
            return {'message': "Instance type not provided or incorrect instance type provide.Valid values are ec2 and rds."}
            
        if "instance_name" not in event:
            print("Instance name not provided")
            return {'message': "Instance name not provided."}
        if "command" not in event or event['command'] not in ["start","status"]:
            print("Command not provided or incorrect command provided.Valid values are start and status")
            return {'message': "Command not provided or incorrect command provided.Valid values are start and status."}
        
        search_word = event["instance_name"]
        if event['instance_type']=="ec2":
            response = ec2_client.describe_instances()
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    for tag in instance['Tags']:
                        if tag['Key'] == 'Name' and search_word in tag['Value']:
                            instances.append(instance)
            if len(instances) == 0:
                print("EC2 Instance not found")
                return {'message': "EC2 Instance not found"}
            
            if event['command'] == "start":
                for instance in instances:
                    if instance['State']['Name']!= 'running':
                        print("Starting instance "+instance['InstanceId']+" upon user request")
                        ec2_client.start_instances(InstanceIds=[instance['InstanceId']])
                return {'message': "Instance start request executed."}
            
            if event['command'] == "status":
                instance_status={}
                for instance in instances:
                    instance_name=""
                    instance_name=next((tag['Value'] for tag in instance['Tags'] if tag['Key'] == 'Name'), 'N/A')
                    instance_status[instance_name]=instance['State']['Name']
                print(instance_status)
                return {'message': instance_status}
                
        elif event['instance_type']=="rds":
            db_cluster_identifier=''
            response = rds_client.describe_db_clusters()
            for dbcluster in response['DBClusters']:
                if search_word in dbcluster['DBClusterIdentifier']:
                    db_cluster_identifier=dbcluster['DBClusterIdentifier']
                    db_cluster_state=dbcluster['Status']
                    break
            if db_cluster_identifier=='':
                print("RDS Instance not found")
                return {'message': "RDS Instance not found"}
            if event['command'] == "start":
                response = rds_client.start_db_cluster(DBClusterIdentifier=db_cluster_identifier)
                print("RDS Instance start request executed.It may take 10-15 minutes before instance is ready")
                return {'message': "RDS Instance start request executed.It may take 15-20 minutes before instance is ready"}
            if event['command'] == "status":
                return {'message':db_cluster_identifier+" is in "+ db_cluster_state+" state"}
            
    #Start all stopped instance and stop all running instances.        
    else:
        response = ec2_client.describe_instances()
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instances.append(instance)
        
        for instance in instances:
            #response = ec2_client.describe_instance_status(InstanceIds=[instance['InstanceId']],IncludeAllInstances=True)
            print(instance['InstanceId'],instance['State']['Name'])
            if instance['State']['Name']!= 'running':
                print("Starting instance "+instance['InstanceId'])
                ec2_client.start_instances(InstanceIds=[instance['InstanceId']])
            else:
                print("Stopping instance "+instance['InstanceId'])
                ec2_client.stop_instances(InstanceIds=[instance['InstanceId']])
      
#Sample Test events
#{}

#{"instance_type":"rds",
#"instance_name":"database-2",
#"command":"status"
#}

#{"instance_type":"ec2",
#"instance_name":"bamboo",
#"command":"status"
#}

#{"instance_type":"ec2",
#"instance_name":"bamboo",
#"command":"start"
#}
