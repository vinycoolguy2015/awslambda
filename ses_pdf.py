from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

import boto

msg = MIMEMultipart()
msg['Subject'] = 'weekly report'
msg['From'] = 'vinayak_pandey@xyz.com'
msg['To'] = 'vinayak@xyz.com'

# what a recipient sees if they don't use an email reader
msg.preamble = 'Multipart message.\n'

# the message body
part = MIMEText('Howdy -- here is the data from last week.')
msg.attach(part)

# the attachment
part = MIMEApplication(open('/tmp/SEP_2015.pdf', 'rb').read())
part.add_header('Content-Disposition', 'attachment', filename='weekly_report.pdf')
msg.attach(part)

# connect to SES
connection = boto.connect_ses()

# and send the message
result = connection.send_raw_email(msg.as_string()
    , source=msg['From']
    , destinations=[msg['To']])
print(result)
