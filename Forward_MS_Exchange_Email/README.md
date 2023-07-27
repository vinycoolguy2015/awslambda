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

