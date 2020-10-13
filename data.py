#!/usr/bin/python

import MySQLdb
import xlwt
import time

try:
    db = MySQLdb.connect("localhost","root","newpass","strack" )
except:
    print("Error connecting to the database")
    exit()
prof_record={}
cursor = db.cursor()
query = ("select distinct lab_id from users_to_labs where status=1 and partner_name='UPES' and is_evaluated=0")
cursor.execute(query)
for lab_id in cursor:
    labid=str(lab_id[0])
    lab_record={}
    professor=''
    students=[]
    query = ("select login from labs where id="+labid)
    cursor.execute(query)
    for data in cursor:
        professor=data[0]
    query = ("select login,sem,course,batch,lesson,lang,date_completed from users_to_labs where status=1 and partner_name='UPES' and is_evaluated=0 and lab_id="+labid)
    cursor.execute(query)
    for student in cursor:
        record={}
        record['Login']=student[0]
        record['Sem']=student[1]
        record['Course']=student[2]
        record['Batch']=student[3]
        record['Lesson']=student[4]
        record['Lang']=student[5]
        record['Date_Completed']=time.strftime("%Y-%m-%d", time.gmtime(float(student[6])))
        students.append(record)
    lab_record[labid] = students
    if professor in prof_record:
        prof_record[professor][labid]=students
    else:
        prof_record[professor]=lab_record
if '' in prof_record:
    data=prof_record['']
del prof_record['']
cursor.close()
db.close()
for key in prof_record.keys():
    i=2
    professor=key
    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Sheet 1")
    style = xlwt.easyxf('pattern: pattern solid, fore_colour light_blue;'
                              'font: colour white, bold True;')
    sheet1.write(0, 0, 'Lab ID',style)
    sheet1.write(0, 1, 'Student ID',style)
    sheet1.write(0, 2, 'Course',style)
    sheet1.write(0, 3, 'Semester',style)
    sheet1.write(0, 4, 'Batch',style)
    sheet1.write(0, 5, 'Lesson',style)
    sheet1.write(0, 6, 'Language',style)
    sheet1.write(0, 7, 'Date_Completed',style)
    data=prof_record[key]
#   print(professor+" has pending approvals for "+str(data))
    for key in data.keys():
        sheet1.write(i, 0, key,style)
        records=data[key]
        for record in records:
            sheet1.write(i, 1, record['Login'])
            sheet1.write(i, 2, record['Course'])
            sheet1.write(i, 3, record['Sem'])
            sheet1.write(i, 4, record['Batch'])
            sheet1.write(i, 5, record['Lesson'])
            sheet1.write(i, 6, record['Lang'])
            sheet1.write(i, 7, record['Date_Completed'])
            i+=1
    book.save(professor+".xls")        

            
