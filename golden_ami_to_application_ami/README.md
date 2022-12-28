1-Create an Aurora MySQL instance to store Golden AMI data.Execute Following commands to create database, table and insert some data.

```
CREATE DATABASE test;
USE test;

CREATE TABLE ami(
   Region     VARCHAR (20)        NOT NULL,
   OperatingSystem VARCHAR (20)     NOT NULL,
   ImageId  VARCHAR (30)             NOT NULL,
   ImageDate DATE   ,
   CreationDate DATETIME   , 
   LastUpdateDate DATETIME   , 
   PRIMARY KEY (ImageId )
);

INSERT INTO ami
VALUES ('us-east-1', 'AmazonLinux2','ami-0b5eea76982371e92' ,'2022-11-01','2022-11-20 17:18:50','2022-11-20 17:18:50' );

INSERT INTO ami
VALUES ('us-east-1', 'AmazonLinux2','ami-0b5eea76982371e91' ,'2022-12-01','2022-12-20 17:18:50','2022-12-20 17:18:50' );


  CREATE TABLE application_ami(
  Region     VARCHAR (20)        NOT NULL,
   OperatingSystem VARCHAR (20)     NOT NULL,
   ImageId  VARCHAR (30)             NOT NULL,
   ImageDate DATE,   
   PRIMARY KEY (ImageId )
);
```

2- Create a secret named db in Secret Manager and store following information:
```
username	admin
password	<RDS_ADMIN_PASSWORD>
dbname	test
host	<RDS_ENDPOINT>
port	3306
```

3-Create an IAM Role for Lambda(lambda.amazonaws.com) and Step Function(states.amazonaws.com) with full admin permission(in a production environment, grant granular access instead of Admin access).

4-Create a CloudFormation stack named Pipeline using image_builder.yml.Change the values for SubnetId and VpcId in the template. This will create a image builder pipeline which we can use for creating application AMI.

5-Create state machine using definition given in state_machine.json. Replace <ACCOUNT_ID> with your AWS Account ID.

6-Create following Lambda functions and use the same role which we created in Step3:

```
Name: get_ami_id
Code File: get_ami_id.py
TimeOut: 1 minute
Environment Variables:
   OS_TYPE	AmazonLinux2
   SECRET_NAME	db
   
Name: update_cft_stack
Code File:  update_cft_stack.py
Timeout:15 minutes
Environment Variables:
   STACK_NAME	Pipeline
   
Name: trigger_image_pipeline
Code File: trigger_image_pipeline.py
Timeout: 2 minutes
Environment Variables:
   STACK_NAME	Pipeline
   
Name: check_image_status
Code File: check_image_status.py
Timeout: 1 minute

Name: store_application_ami_id
Code File: store_application_ami_id.py
Timeout: 5 Minutes
Environment Variables:
   OS_TYPE	AmazonLinux2
   SECRET_NAME	db
```
Please note that store_application_ami_id and get_ami_id needs pymysql package which is not available by default in Lambda.So you need to create a zip package(with pymysql installed) following the instruction given at https://docs.aws.amazon.com/lambda/latest/dg/python-package.html#python-package-create-package-with-dependency and upload the zip as Lambda code. 

7-Trigger the Step function manually and check for the progress. Once it's executed successfully, connect to your RDS instance and check application_ami table in test database.







