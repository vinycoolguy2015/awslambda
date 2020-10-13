'''
select distinct login from user_role order by login INTO OUTFILE '/tmp/user_role1.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';

select distinct login from user_role order by login INTO OUTFILE '/tmp/user_role2.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';


'''



import xlrd
import os

dataDir="C:\\Users\\vinayak.p\\Documents"
dataFile="user_role.xls"
file=os.path.join(dataDir,dataFile)

def parse_file(datafile):
    missing_data=[]
    workbook=xlrd.open_workbook(datafile)
    sheet=workbook.sheet_by_index(0)
    
    for i in range(sheet.nrows):
        found=False
        for j in range(sheet.nrows):
            if str(sheet.cell(j, 0))==str(sheet.cell(i, 1)):
                found=True
                break
        
        if found==False:
            missing_data.append(str(sheet.cell_value(i, 1)))
    return missing_data

data=parse_file(file)
for record in data:
    print record
        
    
    
    
