Reference:https://aws.amazon.com/blogs/messaging-and-targeting/forward-incoming-email-to-an-external-destination/

Additional Resource: https://medium.com/naukri-engineering/use-amazon-ses-to-receive-emails-in-s3-and-forward-incoming-email-to-any-external-email-id-84ffb394c70e

As per https://docs.aws.amazon.com/general/latest/gr/ses.html, incoming mail is only available in 

US East (N. Virginia)	us-east-1	
US West (Oregon)	us-west-2	
Europe (Ireland)	eu-west-1	

If you are using us-east-1	for receiving mail and any other region endpoint for sending mail, then the domain should be whitelisted in both 
regions.

Lambda code given in the doc forwards the mail as attachment which is not ideal. Lambda code to forward mail properly is given here.
Few modifications can be done to this code like creating a folder in /tmp and then downloading the files.Once the mail is sent, delete the folder.

In SES Recipient condition, add email and set object prefix as incoming.

In Lambda, set following environment variables:

MailRecipient	awsplay@gmail.com
MailS3Bucket	email-forwarding
MailS3Prefix	incoming
MailSender	noreply@xyz.com
Region	us-east-1
