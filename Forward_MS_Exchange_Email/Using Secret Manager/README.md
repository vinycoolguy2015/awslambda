Previous setup is using Parameter Store. If you want to use Secret Manager,Do following things

1-Remove VPC EndPoint Creation from networking.yml

2-Move SSM VPC Endpoin to windows.yml

3-Use these lambda.yml and code files
