Create 1 NAT instance using amzn-ami-vpc-nat-2018.03.0.20200918.0-x86_64-ebs AMI. 

ip Lambda should have 30 seconds timeout and specify VPC settings so that it runs within a subnet which uses NAT instance to access internet.

trigger lambda should have 3 minutes as timeout.
