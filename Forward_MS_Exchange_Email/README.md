Reference

* https://www.activestate.com/resources/quick-reads/how-to-install-and-use-exchangelib-python/
* https://medium.com/thg-tech-blog/youve-got-mail-email-analytics-with-python-and-exchange-7ae152443957
* https://docs.aws.amazon.com/lambda/latest/dg/python-package.html
* https://ecederstrand.github.io/exchangelib/ 

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

# Disable the warning for Unverified HTTPS requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)








