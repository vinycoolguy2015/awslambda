import os
import boto3
import email
import sys
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


client_s3 = boto3.client("s3")
client_ses = boto3.client("ses")

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
    incoming_email_prefix = os.environ['MailS3Prefix']
    sender = os.environ['MailSender']
    recipient = os.environ['MailRecipient']
    message_id = event['Records'][0]['ses']['mail']['messageId']
    
    try:
        for file in os.scandir('/tmp'):
            os.remove(file.path)
        if incoming_email_prefix:
            object_path = (incoming_email_prefix + "/" + message_id)
        else:
            object_path = message_id
        
        print("Processing message "+object_path)
    
        # Get the email object from the S3 bucket.
        object_s3 = client_s3.get_object(Bucket=incoming_email_bucket,Key=object_path)
    
        # Read the content of the message.
        file_content = object_s3['Body'].read()

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
    except Exception as error:
        print("An exception occurred:", error)
        send_email("Mail Delivery Notification",message_id+" could not be processed successfully.")
        for file in os.scandir('/tmp'):
            os.remove(file.path)
        sys.exit(0)
        
    
    try:
        # Send the email
        response = client_ses.send_raw_email(RawMessage={"Data": msg.as_string()})
        print(response)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("Mail Sent.Deleting "+object_path+" from S3 bucket and /tmp")
            client_s3.delete_object(Bucket=incoming_email_bucket,Key=object_path)
            os.remove("/tmp/"+message_id)
        else:
            send_email("Mail Delivery Notification",message_id+" was processed but encountered invalid status code during mail forwarding.")
    except Exception as error:
        print("An exception occurred:", error)
        send_email("Mail Delivery Notification",message_id+" was processed but encountered error during mail forwarding.")
    finally:
        for file in os.scandir('/tmp'):
            os.remove(file.path)
        
# Environment variables will be like this
#ErrorNotificationRecipients	error1@xyz.com,error2@xyz.com
#MailRecipient	recipient@xyz.com
#MailS3Bucket	email-forwarding
#MailS3Prefix	incoming
#MailSender	abc@xyz.com
        
    
