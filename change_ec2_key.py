#For setting up OpenSSH on windows follow https://winscp.net/eng/docs/guide_windows_openssh_server to setup Openssh.You need to create .ssh and #ssh/known_hosts under you home directory.

#Script to Change Prod Keys every month

import boto.ec2
from boto.manage.cmdshell import sshclient_from_instance
import datetime


lastmonth = (datetime.date.today().replace(day=1) - datetime.timedelta(days=1)).strftime("%B")
lastyear = (datetime.date.today().replace(day=1) - datetime.timedelta(days=1)).year
lastkey="server"+lastmonth+str(lastyear)

month = datetime.datetime.now().strftime("%B")
year = datetime.date.today().year
keyname="server"+month+str(year)

generate_key_command='ssh-keygen -t rsa -N "" -f '+ keyname+'.pem;chmod 400 '+keyname+'.pem'
add_key_command='ssh-keygen -f '+ keyname+'.pem -y >> ~/.ssh/authorized_keys'
mail_command= 'mail -a '+keyname+'.pem -s "server Key" -r "Prod_KeyChange" vinayak.p@xyz.com <<< "Attached is the new key for iTrack"'
modify_prod_deployment_script_command="sed -i -e 's/"+lastkey+"/"+keyname+"/g' test.sh"
copy_key_command='scp -i '+lastkey+'.pem '+keyname+'.pem ec2-user@x.x.x.x:/home/ec2-user'
modify_permission='chmod 400 '+keyname+'.pem'

access_key=''
secret_access_key=''

conn = boto.ec2.connect_to_region('us-east-1',aws_access_key_id=access_key,aws_secret_access_key=secret_access_key)

instance = conn.get_all_instances(['i-x'])[0].instances[0]

ssh_client = sshclient_from_instance(instance,'C:\Program Files (x86)\OpenSSH\etc\\November2016.pem',user_name='ec2-user')

status, stdout, stderr = ssh_client.run(generate_key_command)
if status ==0:
    print("New key generated")
status, stdout, stderr = ssh_client.run(add_key_command)
if status ==0:
    print("New key added to the authorized keys")
status, stdout, stderr = ssh_client.run(mail_command)
if status ==0:
    print("New key mailed")
status, stdout, stderr = ssh_client.run(modify_prod_deployment_script_command)
if status ==0:
    print("Deployment script changed")
status, stdout, stderr = ssh_client.run(copy_key_command)
if status ==0:
    print("New key copied to Prod2 server")


#Add the newly generated key to the Prod2 server

instance = conn.get_all_instances(['i-xyz'])[0].instances[0]
ssh_client = sshclient_from_instance(instance,'C:\Program Files (x86)\OpenSSH\etc\\November2016.pem',user_name='ec2-user')
status, stdout, stderr = ssh_client.run(modify_permission)
status, stdout, stderr = ssh_client.run(add_key_command)
if status ==0:
    print("New key added to the Prod2 server")







