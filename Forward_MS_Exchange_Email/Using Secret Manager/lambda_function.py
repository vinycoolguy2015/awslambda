import os
import sys
import email
import json 
import smtplib
import urllib3
import boto3
import urllib.request
from exchangelib import DELEGATE, Account, Credentials, Configuration, NTLM
from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

aws_session_token = os.environ.get('AWS_SESSION_TOKEN')

def lambda_handler(event, context):
    req = urllib.request.Request("http://localhost:2773//secretsmanager/get?secretId="+os.environ['ENV_SECRET'])
    req.add_header('X-Aws-Parameters-Secrets-Token', aws_session_token)
    config = urllib.request.urlopen(req).read()
    secret_data= json.loads(config)['SecretString']
    environment_variables=json.loads(secret_data)
    
    # Exchange Server Details
    EXCHANGE_USERNAME = environment_variables['EXCHANGE_USERNAME']
    EXCHANGE_PASSWORD = environment_variables['EXCHANGE_PASSWORD']
    EXCHANGE_SERVER = environment_variables['EXCHANGE_SERVER']
    EXCHANGE_EMAIL = environment_variables['EXCHANGE_EMAIL']
    # AWS SMTP Credentils
    SMTP_HOST=environment_variables['SMTP_HOST']
    SMTP_PASSWORD=environment_variables['SMTP_PASSWORD']
    SMTP_PORT=environment_variables['SMTP_PORT']
    SMTP_USER=environment_variables['SMTP_USER']
    # Mail Recipient And Sender
    SENDER_EMAIL=environment_variables['SENDER_EMAIL']
    RECIPIENT_EMAIL=environment_variables['RECIPIENT_EMAIL']
    ERROR_EMAIL_RECIPIENT=environment_variables['ERROR_EMAIL_RECIPIENT']

    BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    try:
        credentials = Credentials(username=EXCHANGE_USERNAME, password=EXCHANGE_PASSWORD)
        config = Configuration(server=EXCHANGE_SERVER, credentials=credentials, auth_type=NTLM)
        account = Account(primary_smtp_address=EXCHANGE_EMAIL, config=config,autodiscover=False, access_type=DELEGATE)
    except Exception as ex:
        print(ex)
        subject = 'Error Connecting To '+EXCHANGE_EMAIL+' Mailbox'
        body = 'Could not connect to '+EXCHANGE_EMAIL+' Mailbox.Please check the credentials and connectivity'
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = ERROR_EMAIL_RECIPIENT
        server = smtplib.SMTP(host=SMTP_HOST, port=SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SENDER_EMAIL,msg['To'].split(","), msg=msg.as_string())
        server.close()
        sys.exit(0)
    else:
        inbox = account.inbox
    #for item in inbox.all().order_by('-datetime_received')[:2]:
    for item in inbox.all().order_by('-datetime_received'):
        print('Processing following email. Subject:'+str(item.subject)+',Sender:'+ str(item.sender)+',Date:'+ str(item.datetime_received))
        for file in os.scandir('/tmp'):
            os.remove(file.path)
        body=""
        print("----------------------------------------")
        #print(item.subject, item.sender, item.datetime_received)
        if item.text_body:
            #print(f"Body: {item.text_body}")
            body=item.text_body
        elif item.html_body:
            #print(f"Body (HTML): {item.html_body}")
            body=item.html_body
        else:
            print("No body found.")

        # Fetch email attachments
        if item.attachments:
            for attachment in item.attachments:
                if attachment.is_inline:
                    # Skip inline attachments (e.g., images in the email body)
                    continue
                file_name = attachment.name
                with open("/tmp/"+file_name, 'wb') as f:
                    f.write(attachment.content)
                print(f"Attachment saved: {file_name}")
        else:
            print("No attachments found.")
        
        print("----------------------------------------")
        msg = MIMEMultipart()
        msg["Subject"] = item.subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECIPIENT_EMAIL
        msg["Reply-To"] = item.sender.email_address
        msg.attach(MIMEText(item.text_body))

        # Add the attachments
        for attachment_received in item.attachments:
            if attachment_received.is_inline:
                continue
            with open("/tmp/"+attachment_received.name, "rb") as f:
                attachment = MIMEApplication(f.read(), _subtype="png")
                attachment.add_header("Content-Disposition", "attachment", filename=os.path.basename(attachment_received.name))
                msg.attach(attachment)
        #s.sendmail(os.environ['MailSender'],os.environ['MailRecipient'], msg.as_string())
        try:
            server = smtplib.SMTP(host=SMTP_HOST, port=SMTP_PORT)
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SENDER_EMAIL,RECIPIENT_EMAIL, msg=msg.as_string())
            #server.close()
        except Exception as ex:
            print(ex)
            subject = 'Error In Forwarding Email For '+EXCHANGE_EMAIL+' Mailbox'
            body = 'Lambda failed to forward following email. Subject:'+str(item.subject)+',Sender:'+ str(item.sender)+',Date:'+ str(item.datetime_received)
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = SENDER_EMAIL
            msg['To'] = ERROR_EMAIL_RECIPIENT
            server.sendmail(SENDER_EMAIL,msg['To'].split(","), msg=msg.as_string())
            forwarding_failed_folder = account.root / 'Top of Information Store' / 'Forwarding-Failure'
            item.move(forwarding_failed_folder)
        else:
            #item.delete()
            archive_folder = account.root / 'Top of Information Store' / 'Archive'
            item.move(archive_folder)
        finally:
            server.close()
        



