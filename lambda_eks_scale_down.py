"Lambda function list pods in EKS cluster"
import base64
import os
import logging
import re
import boto3
from pprint import pprint
from kubernetes.client.rest import ApiException

from botocore.signers import RequestSigner
from kubernetes import client, config


logger = logging.getLogger()
logger.setLevel(logging.INFO)

STS_TOKEN_EXPIRES_IN = 60
session = boto3.session.Session()
sts = session.client('sts')
service_id = sts.meta.service_model.service_id
#cluster_name = _event["CLUSTER_NAME"]
eks = boto3.client('eks')

deployment_info = {
    "eks-cluster1": {
        "default": {
            "nginx": 0
        },
        "test": {
            "nginx2":0
        }
    },
    "eks-cluster2": {
        "default": {
            "nginx": 0
        },
        "test": {
            "nginx2": 0,
            "nginx3": 0
        }
    }
}

cronjob_info = {
    "eks-cluster1": {
        "default": ["job1"],
        "test": ["job2"]
    },
    "eks-cluster2": {
        "default": ["job1"]
    }
}


def get_cluster_info(cluster_name):
    "Retrieve cluster endpoint and certificate"
    cluster_info = eks.describe_cluster(name=cluster_name)
    endpoint = cluster_info['cluster']['endpoint']
    cert_authority = cluster_info['cluster']['certificateAuthority']['data']
    cluster_info = {
        "endpoint" : endpoint,
        "ca" : cert_authority
    }
    return cluster_info

def get_bearer_token(cluster_name):
    "Create authentication token"
    signer = RequestSigner(
        service_id,
        session.region_name,
        'sts',
        'v4',
        session.get_credentials(),
        session.events
    )

    params = {
        'method': 'GET',
        'url': 'https://sts.{}.amazonaws.com/'
               '?Action=GetCallerIdentity&Version=2011-06-15'.format(session.region_name),
        'body': {},
        'headers': {
            'x-k8s-aws-id': cluster_name
        },
        'context': {}
    }

    signed_url = signer.generate_presigned_url(
        params,
        region_name=session.region_name,
        expires_in=STS_TOKEN_EXPIRES_IN,
        operation_name=''
    )
    base64_url = base64.urlsafe_b64encode(signed_url.encode('utf-8')).decode('utf-8')

    # remove any base64 encoding padding:
    return 'k8s-aws-v1.' + re.sub(r'=*', '', base64_url)


def lambda_handler(_event, context):
    "Lambda handler"
    cluster_name = _event["CLUSTER_NAME"]
    cluster = get_cluster_info(cluster_name)

    kubeconfig = {
        'apiVersion': 'v1',
        'clusters': [{
          'name': 'cluster1',
          'cluster': {
            'certificate-authority-data': cluster["ca"],
            'server': cluster["endpoint"]}
        }],
        'contexts': [{'name': 'context1', 'context': {'cluster': 'cluster1', "user": "user1"}}],
        'current-context': 'context1',
        'kind': 'Config',
        'preferences': {},
        'users': [{'name': 'user1', "user" : {'token': get_bearer_token(cluster_name)}}]
    }

    config.load_kube_config_from_dict(config_dict=kubeconfig)
    apps_v1 = client.AppsV1Api()
    batch_v1=client.BatchV1Api()
    print("Changing Deployment")
    try:
        for cluster, namespace in deployment_info.items():
            if cluster == cluster_name:
                for namespace_name, deployment in namespace.items():
                    for deployment_name, replica_count in deployment.items():
                        response = apps_v1.patch_namespaced_deployment_scale(deployment_name, namespace_name,[{'op': 'replace', 'path': '/spec/replicas', 'value': replica_count}])
                    pprint(response)
                break
    except ApiException as e:
        print("Exception when calling AppsV1Api->patch_namespaced_deployment_scale: %s\n" % e)
    print("Changing CronJob")
    try:
        for cluster, namespace in cronjob_info.items():
            if cluster == cluster_name:
                if isinstance(namespace, dict):
                    for namespace_name,cronjobs  in namespace.items():
                        for cronjob in cronjobs:
                            print(cluster,namespace_name,cronjob)
                            response = batch_v1.patch_namespaced_cron_job(cronjob, namespace_name,[{'op': 'replace', 'path': '/spec/suspend', 'value': True}])
                            pprint(response)
                break
    except ApiException as e:
        print("Exception when calling BatchV1Api->patch_namespaced_cron_job: %s\n" % e)
