We can also do the same setup via CloudFormation. Instructions are given below:

Pre-requisites:
* SES Domain verification and sandbox waiver should already be done
* Archive and Forwarding-Failed folder should be there in mailbox as it's hardcoded in the code.
* SMTP user credentials should already be generated
* S3 bucket to upload Zipped Lambda code should already be created.
* Once CFT is executed, Populate Parameter Store with all required Lambda variables. Value of the Parameter Store should look like this:

```
{
      "ERROR_EMAIL_RECIPIENT": "<Email Addresses To Send Mail When Lambda Fails To Process An Email. Format is abc@abc.com,def@abc.com>",
      "EXCHANGE_EMAIL": "<Email Address Associated With Exchange Account>",
      "EXCHANGE_PASSWORD": "<Exchange Account Password>",
      "EXCHANGE_SERVER": "<Exchange Server Address Without HTTPS.For example mail.mycorp.com>",
      "EXCHANGE_USERNAME": "<Exchange Account Username.If there is \ in the username, it should be escaped as \\>",
      "RECIPIENT_EMAIL": "<Email Address To Forward Email To>",
      "SENDER_EMAIL": "<Email Address To Send Email From>",
      "SMTP_HOST": "<email-smtp.us-east-1.amazonaws.com>",
      "SMTP_PASSWORD": "<AWS SMTP User Password>",
      "SMTP_PORT": "587",
      "SMTP_USER": "<AWS SMTP Username>"
    }
```
CFT Teamplete Will do following things
* Create SMTP and SSM VPC EndPoint and Security Group Allowing traffic on port 443 for the CIDR Given
* Read zip code from S3 and create Lambda function
* Create 1 SNS Topic and Create CloudWatch Alarm for Lambda Error
* Create CloudWatch event trigger
* Create Parameter store to store environment variables

Lambda package was generated with following commands:

```
pip3.10 install --target ./package exchangelib
pip3.10 install --target ./package boto3

```

