#! /bin/bash

sleep 180
yum update -y
yum install -y mysql git jq

yum install -y gcc-c++ make
curl -sL https://rpm.nodesource.com/setup_14.x | sudo -E bash -
yum install -y nodejs

#git clone https://github.com/chapagain/nodejs-mysql-crud
git clone https://github.com/vinycoolguy2015/nodejs-mysql-crud.git
rds_hostname=`aws rds describe-db-instances --region us-east-1 |jq [.DBInstances[0].Endpoint.Address][0]| tr -d '"'`
#rds_status=`aws rds describe-db-instances --region us-east-1 |jq [.DBInstances[0].DBInstanceStatus][0]| tr -d '"'`
if [ $rds_hostname == "null" ]; then  sleep 5m;fi
rds_hostname=`aws rds describe-db-instances --region us-east-1 |jq [.DBInstances[0].Endpoint.Address][0]| tr -d '"'`

cd nodejs-mysql-crud
sed -i "s/localhost/$rds_hostname/g" config.js
node app.js

