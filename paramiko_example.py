#!/usr/bin/env python
import paramiko
import os
hostname = '52.xx.xx.xx'
port = 22
username = 'centos'
dir_path = '/home/centos/logs/'
key = paramiko.RSAKey.from_private_key_file("C:\\Users\\vinayak\\Downloads\\Key.pem")

if __name__ == "__main__":
	t = paramiko.Transport((hostname, port))
	t.connect(username=username, pkey=key)
	sftp = paramiko.SFTPClient.from_transport(t)
	
	files = sftp.listdir(dir_path)
	for f in files:
			print 'Retrieving', f
			sftp.get(os.path.join(dir_path, f), f)
	t.close()
	
	
	
