import os
import boto3
import email
import re
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

region = os.environ['Region']

def lambda_handler(event, context):

    incoming_email_bucket = os.environ['MailS3Bucket']
    incoming_email_prefix = os.environ['MailS3Prefix']
    
    message_id = event['Records'][0]['ses']['mail']['messageId']

    if incoming_email_prefix:
        object_path = (incoming_email_prefix + "/" + message_id)
    else:
        object_path = message_id
    
    # Create a new S3 client.
    client_s3 = boto3.client("s3")
    client_ses = boto3.client("ses",region_name='ap-southeast-1')

    # Get the email object from the S3 bucket.
    object_s3 = client_s3.get_object(Bucket=incoming_email_bucket,
        Key=object_path)
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


    sender = os.environ['MailSender']
    recipient = os.environ['MailRecipient']


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

