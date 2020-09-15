#Add Following packages in requirements.txt
#sendgrid
#google-cloud-dataproc==0.5.0

def email(from_email,to_email,subject,content):
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail, Email
    from python_http_client.exceptions import HTTPError
    import os
    
    sg = SendGridAPIClient(os.environ['email_api_key'])
    message = Mail( from_email=from_email,to_emails=to_email,subject=subject,html_content=content)
    try:
        response = sg.send(message)
    except HTTPError as e:
        return e

def dataproc_monitoring(context):
    from google.cloud import dataproc_v1
    from google.cloud.dataproc_v1.gapic.transports import job_controller_grpc_transport
    import time
    import os

    epoch_time = int(time.time())
    check_jobs_failed_in_seconds=300 # Will be used to check dataproc jobs failed in last 5 minutes.You can increase this limit as per the requirement.
    project_id = os.environ['GCP_PROJECT']
    region = 'us-central1'
	
    job_transport = job_controller_grpc_transport.JobControllerGrpcTransport(address='us-central1-dataproc.googleapis.com:443')
    jobs_client = dataproc_v1.JobControllerClient(job_transport)
    for job in jobs_client.list_jobs(project_id,region):
        if job.status.State.Name(job.status.state) == 'ERROR' and job.status.state_start_time.seconds >= (epoch_time-check_jobs_failed_in_seconds):
            #print(job.reference.job_id)
            email('abc@gmail.com','efg@gmail.com','DataProc Job Failed','<strong>'+job.reference.job_id+' job failed.</strong>')
        else:
            print(job.reference.job_id,job.status.State.Name(job.status.state))	    
