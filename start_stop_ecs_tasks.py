import boto3


def lambda_handler(event, context):
    client = boto3.client('ecs')
    response = client.list_clusters()
    for cluster in response['clusterArns']:
        service_list = client.list_services(cluster=cluster,launchType='FARGATE')
        for service in service_list['serviceArns']:
            if event['action']=='stop':
                client.update_service(cluster=cluster,service=service,desiredCount=0)
                print("Stopped service "+service)
            elif event['action']=='start':
                client.update_service(cluster=cluster,service=service,desiredCount=1)
                print("Started service "+service)
