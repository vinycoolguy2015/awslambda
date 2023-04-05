Reference:https://aws.amazon.com/blogs/messaging-and-targeting/forward-incoming-email-to-an-external-destination/

As per https://docs.aws.amazon.com/general/latest/gr/ses.html, incoming mail is only available in 

US East (N. Virginia)	us-east-1	
US West (Oregon)	us-west-2	
Europe (Ireland)	eu-west-1	

If you are using us-east-1	for receiving mail and any other region endpoint for sending mail, then the domain should be whitelisted in both 
regions.

Lambda code given in the doc forwards the mail as attachment which is not ideal. Lambda code to forward mail properly is given here.
