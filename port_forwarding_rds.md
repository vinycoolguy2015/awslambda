If we want to connect to our RDS instances from our local machine, we can first connect to an instance and then start a port-forwarding session to our RDS instance. Let's see how to do this:

SSM agent on Bamboo instance should be the updated version. We can update the agent using following commands:
  ```
  sudo yum update amazon-ssm-agent
  sudo systemctl daemon-reexec
  sudo systemctl restart amazon-ssm-agent.service
  ```
 
Now start a port forwarding session

```
aws ssm start-session --target <instance_id> --document-name AWS-StartPortForwardingSessionToRemoteHost --parameters '{"portNumber":["5432"],"localPortNumber":["1053"],"host":[<RDS_HOSTNAMe>]}'
```

Now connect to RDS using
```
psql -h localhost -p 1053 -U admin -d database_name
```
