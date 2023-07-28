Create a Lambda function with Python 3.7 runtime with the code given at my_deployment_package.zip

Make sure Lambda has connectivity to MS Exchange Server

Lambda Code was tested in an environement with no internet connectivity. So a VPC Endpoint for com.amazonaws.us-east-1.email-smtp was created.

Following Lambda Environment Variables are required:

* ERROR_MAIL_RECIPIENT	     #Email Address To Send Mail When Lambda Fails To Process An Email
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

Reference:https://docs.aws.amazon.com/lambda/latest/dg/python-package.html

pip3 install --target ./package exchangelib

pip3 install --target ./package urllib3==1.26.6 --upgrade


Update: For Python 3.9 Lambda runtime, create an EC2 instance with Amazon Linux2 AMI and follow https://computingforgeeks.com/how-to-install-python-on-amazon-linux/ to install Python3.9. For Python 3.10, follow https://techviewleo.com/how-to-install-python-on-amazon-linux-2

Then run pip3.9 install --target ./package exchangelib.

For Lambda function with Python 3.9 runtime use the code given at my_deployment_package_3.9.zip

Also update ERROR_MAIL_RECIPIENT value as abc@gmail.com,def@gmail.com.Make sure Archive and Forwarding-Failure folders are there in outlook

* https://www.activestate.com/resources/quick-reads/how-to-install-and-use-exchangelib-python/
* https://medium.com/thg-tech-blog/youve-got-mail-email-analytics-with-python-and-exchange-7ae152443957
