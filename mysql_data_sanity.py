def send_mail(msg):
    import smtplib
    from email.mime.text import MIMEText
    msg = MIMEText(msg)
    msg['Subject'] = 'Hash mismatch in data'
    s = smtplib.SMTP('localhost')
    s.sendmail('info@localhost','vinayak.p@abc.com', msg.as_string())
    s.quit()



def main():
    import MySQLdb
    dbProd1 = MySQLdb.connect("localhost","root","password","db" )
    cursorProd1 = dbProd1.cursor()
    dbProd2 = MySQLdb.connect("172.1.3.196","root","password","db" )
    cursorProd2 = dbProd2.cursor()
    queryProd1 = ("SELECT table_name FROM information_schema.tables WHERE table_type = 'base table' AND table_schema='example';")
    cursorProd1.execute(queryProd1)
    mismatched_tables=[]
    for table in cursorProd1:
        query=("checksum table " +table[0]+";")
        countProd1=cursorProd1.execute(query)
        countProd2=cursorProd2.execute(query)
        count1=cursorProd1.fetchone()[1]
        count2=cursorProd2.fetchone()[1]
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
