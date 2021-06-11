#! /bin/bash
sleep 120
yum update -y
yum install git python3-pip python3-devel python3-setuptools wget ruby -y
wget https://aws-codedeploy-ap-southeast-1.s3.ap-southeast-1.amazonaws.com/latest/install
chmod +x ./install
./install auto
service codedeploy-agent start
wget https://s3.amazonaws.com/aaronsilber/public/authbind-2.1.1-0.1.x86_64.rpm
rpm -Uvh https://s3.amazonaws.com/aaronsilber/public/authbind-2.1.1-0.1.x86_64.rpm
touch /etc/authbind/byport/80
chmod 500 /etc/authbind/byport/80
chown ec2-user /etc/authbind/byport/80
git clone https://github.com/vinycoolguy2015/FlaskAppCodeDeploy.git /home/ec2-user/app
chmod +x /home/ec2-user/app/scripts/*
/home/ec2-user/app/scripts/install_app_dependencies
/home/ec2-user/app/scripts/start_server
