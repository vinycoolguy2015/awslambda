#!/usr/bin/python2.7

def send_mail(msg):
    import smtplib
    from email.mime.text import MIMEText
    msg = MIMEText(msg)
    msg['Subject'] = 'Count mismatch in data'
    s = smtplib.SMTP('localhost')
    s.sendmail('server@localhost','vinayak.p@xyz.com', msg.as_string())
    s.quit()



def main():
    import MySQLdb
    dbProd1 = MySQLdb.connect("localhost","root","Track","trackdb2" )
    cursorProd1 = dbProd1.cursor()
    dbProd2 = MySQLdb.connect("172.1.3.196","root","Track","trackdb2" )
    cursorProd2 = dbProd2.cursor()
    queryProd1 = ("SELECT table_name FROM information_schema.tables WHERE table_type = 'base table' AND table_schema='trackdb2';")
    cursorProd1.execute(queryProd1)
    mismatched_tables=[]
    for table in cursorProd1:
        query=("select count(*) from " +table[0]+";")
        countProd1=cursorProd1.execute(query)
        countProd2=cursorProd2.execute(query)
        count1=cursorProd1.fetchone()[0]
        count2=cursorProd2.fetchone()[0]
        if count1 != count2:
            mismatched_tables.append(table[0])
    cursorProd1.close()
    cursorProd2.close()
    dbProd1.close()
    dbProd2.close()
    if len(mismatched_tables)>0:
        msg = ' '.join(mismatched_tables)
        send_mail(msg)

if __name__ == "__main__":
    main()
