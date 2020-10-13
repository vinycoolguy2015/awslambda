import boto
import boto.ec2
import paramiko 
from boto.manage.cmdshell import sshclient_from_instance

access_key=''
secret_access_key=''

conn = boto.ec2.connect_to_region('us-east-1',aws_access_key_id=access_key,aws_secret_access_key=secret_access_key)
instance = conn.get_all_instances(['i-0b51be599192e1780'])[0].instances[0]
ssh_client = sshclient_from_instance(instance,'C:\Program Files (x86)\OpenSSH\etc\\November2016.pem',user_name='ec2-user')
print "Downloading file..."
ssh_client.get_file("/home/ec2-user/November2016.pem",r"C:/Program Files (x86)/OpenSSH/etc/November2016.pem")
