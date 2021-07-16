import boto3



def lambda_handler(event, context):
    ec2 = boto3.client('ec2', 'ap-south-1')
    reservations = ec2.describe_instances(
        Filters=[
            {'Name': 'tag:Env', 'Values': ['Dev']}
        ]
    )
    servers = []
    for instances in reservations['Reservations']:
        for instance in instances['Instances']:
            servers.append(instance['InstanceId'])
    if event['path'] == '/start':
        ec2.start_instances(InstanceIds=servers)
        response = {
		    "statusCode": 200,
		    "statusDescription": "200 OK",
		    "isBase64Encoded": False,
		    "headers": {
			    "Content-Type": "text/html; charset=utf-8"
	    }
	    }

        response['body'] = """<html>
        <head>
        <title>Dev Instance Status</title>
        <style>
        html, body {
        margin: 0; padding: 0;
        font-family: arial; font-weight: 10; font-size: 3em;
        text-align: center;
        }
        </style>
        </head>
        <body>
        <p>Instance Started</p>
        </body>
        </html>"""
        return response
    
        
    elif event['path'] == '/stop':
        ec2.stop_instances(InstanceIds=servers)
        response = {
		    "statusCode": 200,
		    "statusDescription": "200 OK",
		    "isBase64Encoded": False,
		    "headers": {
			    "Content-Type": "text/html; charset=utf-8"
	    }
	    }

        response['body'] = """<html>
        <head>
        <title>Dev Instance Status</title>
        <style>
        html, body {
        margin: 0; padding: 0;
        font-family: arial; font-weight: 10; font-size: 3em;
        text-align: center;
        }
        </style>
        </head>
        <body>
        <p>Instance Stopped</p>
        </body>
        </html>"""
        return response
    
