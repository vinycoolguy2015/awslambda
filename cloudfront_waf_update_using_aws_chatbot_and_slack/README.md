Reference: 

https://aws.amazon.com/blogs/devops/running-aws-commands-from-slack-using-aws-chatbot

Command to execute in Slack channel:

@aws lambda invoke --payload {"domain": "d1cd8l93w", "ipv4": "10.10.10.100","ipv6":"2a09:bac0:9001:20::33:255"} --function-name wafupdate --region us-east-1
