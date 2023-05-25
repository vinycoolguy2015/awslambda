import os
import boto3
import email
import sys
from datetime import datetime, timedelta
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

client_s3 = boto3.client("s3")
client_ses = boto3.client("ses",region_name='ap-southeast-1')

def send_email(error_subject,error_message):
    CHARSET = "UTF-8"
    error_notificationrecipients=os.environ['ErrorNotificationRecipients'].split(",")
    response = client_ses.send_email(
        Destination={
            "ToAddresses": error_notificationrecipients
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                    "Data": error_message,
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": error_subject,
            },
        },
        Source=os.environ['MailSender'],
    )



def lambda_handler(event, context):
    
    incoming_email_bucket = os.environ['MailS3Bucket']
    sender = os.environ['MailSender']
    recipient = os.environ['MailRecipient']
    
    try:
        # Calculate the time threshold
        current_time = datetime.utcnow()
        threshold_time = current_time - timedelta(minutes=30)
        
        response = client_s3.list_objects_v2(Bucket=incoming_email_bucket)
        
        # Iterate over the objects and filter by last modified time
        if "Contents" in response:
            for obj in response["Contents"]:
                last_modified = obj["LastModified"].replace(tzinfo=None)
                # Check if last modified time is greater than threshold
                if last_modified < threshold_time:
                    object_path = obj["Key"]
                    message_id=object_path.split('/')[1]
                    print("Processing "+object_path)
                    # Get the email object from the S3 bucket.
                    object_s3 = client_s3.get_object(Bucket=incoming_email_bucket,Key=object_path)
                    # Read the content of the message.
                    file_content = object_s3['Body'].read()
                    
                    for file in os.scandir('/tmp'):
                        os.remove(file.path)
                    
                    with open("/tmp/"+message_id, "wb") as f:
                        f.write(file_content)
                        f.close()

                    with open("/tmp/"+message_id, "rb") as f:
                        raw_email = f.read()
                        email_message = email.message_from_bytes(raw_email)
                        f.close()
                    # Extract the subject
                    subject = email_message["Subject"]
    
                    # Extract the body
                    body = ""
                    if email_message.is_multipart():
                        for part in email_message.walk():
                            content_type = part.get_content_type()
                            if content_type == "text/plain":
                                body += part.get_payload(decode=True).decode("utf-8")
                            else:
                                payload = email_message.get_payload(decode=True)
                                if payload:
                                    body = payload.decode("utf-8")
                                
                    # Extract the attachments
                    attachments = []
                    if email_message.is_multipart():
                        for part in email_message.walk():
                            content_type = part.get_content_type()
                            filename = part.get_filename()
                            if filename:
                                # Decode the filename if it's encoded
                                filename = email.header.decode_header(filename)[0][0]
                                # Save the attachment to disk
                                with open(os.path.join("/tmp/", filename), "wb") as f:
                                    f.write(part.get_payload(decode=True))
                                attachments.append(filename)
                    # Create a multipart message container
                    msg = MIMEMultipart()
                    msg["Subject"] = subject
                    msg["From"] = sender
                    msg["To"] = recipient
                    msg.attach(MIMEText(body))

                    # Add the attachments
                    attachments = attachments
                    for file_path in attachments:
                        with open("/tmp/"+file_path, "rb") as f:
                            attachment = MIMEApplication(f.read(), _subtype="png")
                            attachment.add_header("Content-Disposition", "attachment", filename=os.path.basename(file_path))
                            msg.attach(attachment)
                   # Send the email
                    response = client_ses.send_raw_email(RawMessage={"Data": msg.as_string()})
                    print(response)
                    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                        print("Successfully forwarded incoming mail.Now deleting "+object_path+" from S3 bucket and /tmp")
                        client_s3.delete_object(Bucket=incoming_email_bucket,Key=object_path)
                        os.remove("/tmp/"+message_id)
                    else:
                        send_email("Mail Delivery Notification",message_id+" was reprocessed but encountered invalid status code during mail forwarding.")
        else:
            print("No failed messages found in the bucket.")
            
    except Exception as error:
        print("An exception occurred:", error)
        send_email("Mail Delivery Notification","Some messages could not be reprocessed successfully.")
        
    finally:
        for file in os.scandir('/tmp'):
            os.remove(file.path)
        
        
        
    
        
    
