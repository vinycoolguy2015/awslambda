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

2- Create a secret named db in Secret Manager and store following information:
```
username	admin
password	<RDS_ADMIN_PASSWORD>
dbname	test
host	<RDS_ENDPOINT>
port	3306
```
3-Create an IAM Role for Lambda(lambda.amazonaws.com) and Step Function(states.amazonaws.com) with full admin permission(in a production environment, grant granular access instead of Admin access).

4-Create an Image Builder Pipeline using image_pipeline.yml

5-Create state machine using definition given in state_machine.json. Replace <ACCOUNT_ID> with your AWS Account ID.

5-


