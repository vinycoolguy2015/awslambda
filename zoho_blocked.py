def check_mailbox(username,password):

    from datetime import datetime, timedelta
    import os
    import email
    import imaplib
    import mailbox
    
    

    date=(datetime.today()- timedelta(days=1)).strftime('%d-%b-%Y')
    mail = imaplib.IMAP4_SSL('imappro.zoho.com')
    mail.login(username, password)
    #folders= mail.list()
    searchdate="(ON \""+date+"\" SUBJECT \"Zoho Mail : Email Outgoing Blocked\")"
    mail.select('mailer-daemon', readonly=True)
    typ, data = mail.search(None, searchdate)
    for num in data[0].split():
        typ, data = mail.fetch(num, '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1].decode('utf-8'))
                varSubject = msg['subject']
                varFrom = msg['from']
                varDate=msg['date']
                date_tuple = email.utils.parsedate_tz(varDate)
                if date_tuple:
                    local_date = datetime.fromtimestamp(
                    email.utils.mktime_tz(date_tuple))
                    if date ==local_date.strftime("%d-%b-%Y"):
                        mailstring='mail -s "'+username+' is blocked" -r "Email_Blocked" vinayak.p@abc.com <<<"Check '+username+' mailbox"'
                        os.system(mailstring)
    mail.logout()

check_mailbox("info@abc.com","abcd")
