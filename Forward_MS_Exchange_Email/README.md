Reference

* https://www.activestate.com/resources/quick-reads/how-to-install-and-use-exchangelib-python/
* https://medium.com/thg-tech-blog/youve-got-mail-email-analytics-with-python-and-exchange-7ae152443957
* https://docs.aws.amazon.com/lambda/latest/dg/python-package.html
* https://ecederstrand.github.io/exchangelib/
* https://docs.aws.amazon.com/secretsmanager/latest/userguide/retrieving-secrets_lambda.html

Create an EC2 instance with Amazon Linux2 AMI and follow https://techviewleo.com/how-to-install-python-on-amazon-linux-2 to install Python 3.10.

Then run pip3.10 install --target ./package exchangelib to generate the required package.Create a Lambda function with Python 3.10
runtime and upoload the zipped code.

Make sure Lambda has connectivity to MS Exchange Server.

Lambda Code was tested in an environement with no internet connectivity. So a VPC Endpoint for com.amazonaws.us-east-1.email-smtp was created.Also create AWS SMTP credentials.

Following Lambda Environment Variables are required:

* ERROR_EMAIL_RECIPIENT	     #Email Addresses To Send Mail When Lambda Fails To Process An Email. Format is abc@abc.com,def@abc.com
* EXCHANGE_EMAIL	           #Email Address Associated With Exchange Account
* EXCHANGE_PASSWORD	         #Exchange Account Password
* EXCHANGE_SERVER	           #Exchange Server Address Without HTTPS.For example mail.mycorp.com
* EXCHANGE_USERNAME	         #Exchange Account Username
* RECIPIENT_EMAIL	           #Email Address To Forward Email To
* SENDER_EMAIL	             #Email Address To Send Email From
* SMTP_HOST	                 email-smtp.us-east-1.amazonaws.com
* SMTP_PASSWORD	             #AWS SMTP User Password
* SMTP_PORT	                 587
* SMTP_USER	                 #AWS SMTP Username

If you see /var/task/urllib3/connectionpool.py:1095: InsecureRequestWarning: Unverified HTTPS request is being made to host error in logs, you can add following lines in the code

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

Once Lambda stack is up,Go to ams-smtp-user user and generate credentials

Go To https://docs.aws.amazon.com/ses/latest/dg/smtp-credentials.html and copy the python code.
    
Execute python3 /tmp/smtp.py <SECRET_ACCESS_KEY> ap-southeast-1 to get SMTP Password(SMTP Username is user's Access Key)
    
Go to secrets manager and update values.

You can also add multiple CC and BCC with following sample code

```
import json
import smtplib,email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

SMTP_HOST="email-smtp.ap-southeast-1.amazonaws.com"
SMTP_PORT=587
SMTP_USER=""
SMTP_PASSWORD=""
SENDER_EMAIL="abc@xyz.com"

def lambda_handler(event, context):
    subject = 'Email Setup'
    body = 'Email Setup'
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = "abc@xyz.com,def@xyz.com"
    msg['CC'] = "ghi@xyz.com,jkl@xyz.com"
    msg['BCC']= "mno@xyz.com,pqr@xyz.com"
    
    MSG_TO_LIST=msg['To'].split(",")
    MSG_CC_LIST=msg['CC'].split(",")
    MSG_BCC_LIST=msg['BCC'].split(",")
    RECEIVER_EMAIL=MSG_TO_LIST+MSG_BCC_LIST
    
    server = smtplib.SMTP(host=SMTP_HOST, port=SMTP_PORT)
    server.starttls()
    server.login(SMTP_USER, SMTP_PASSWORD)
    server.sendmail(SENDER_EMAIL,RECEIVER_EMAIL, msg=msg.as_string())
    server.close()
```
