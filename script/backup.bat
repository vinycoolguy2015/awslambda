@ECHO OFF
REM BFCPEOPTIONSTART
REM Advanced BAT to EXE Converter www.BatToExeConverter.com
REM BFCPEEXE=C:\Users\vinayak.p\Downloads\Backup.exe
REM BFCPEICON=
REM BFCPEICONINDEX=0
REM BFCPEEMBEDDISPLAY=0
REM BFCPEEMBEDDELETE=1
REM BFCPEADMINEXE=0
REM BFCPEINVISEXE=0
REM BFCPEVERINCLUDE=0
REM BFCPEVERVERSION=1.0.0.0
REM BFCPEVERPRODUCT=Product Name
REM BFCPEVERDESC=Product Description
REM BFCPEVERCOMPANY=Your Company
REM BFCPEVERCOPYRIGHT=Copyright Info
REM BFCPEOPTIONEND
@ECHO ON
@echo off
if not exist putty.exe powershell -command "& { iwr https://the.earth.li/~sgtatham/putty/latest/x86/putty.exe -OutFile putty.exe }"
if not exist pscp.exe powershell -command "& { iwr https://the.earth.li/~sgtatham/putty/latest/x86/pscp.exe -OutFile pscp.exe }"
if not exist db.ppk (
Msg * "Please copy the db.ppk file in the current directory"
exit
)
set /p env="Please select the environment: 1(Staging)/2(Production) "
if %env% EQU 1 goto staging
if %env% EQU 2 goto production
pause


:production
@echo rm -rf /home/centos/dump >command.txt
@echo rm -f /home/centos/dump.gz>> command.txt
@echo /usr/bin/mongodump --host prod/db1,db2,db3 -u "backup" -p "Prodbackup1086#" --authenticationDatabase admin>> command.txt
@echo tar -cvzf /home/centos/dump.gz /home/centos/dump >> command.txt
putty -ssh -l centos -i db.ppk -m command.txt x.y.z.z
del command.txt
if not exist c:\backup\ mkdir c:\backup\
if not exist c:\backup\prod\ mkdir c:\backup\prod\
pscp.exe -i db.ppk centos@5x.y.z.z:/home/centos/dump.gz c:\backup\prod\
GOTO End




:staging
@echo rm -rf /home/centos/dump >command.txt
@echo rm -f /home/centos/dump.gz>> command.txt
@echo /usr/bin/mongodump --db db >> command.txt
@echo tar -cvzf /home/centos/dump.gz /home/centos/dump >> command.txt
putty -ssh -l centos -i db.ppk -m command.txt x.y.z.z
del command.txt
if not exist c:\backup\ mkdir c:\backup\
if not exist c:\backupp\staging\ mkdir c:\backup\staging\
pscp.exe -i db.ppk centos@x.y.z.z:/home/centos/dump.gz c:\backup\staging\
GOTO End

:End
Msg * "File has been copied to C:\backup directory"









