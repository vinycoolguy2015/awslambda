1-Create a VPC with Public and Private Subnets. For Private Subnets create VPC Endpoints for 
- com.amazonaws.us-east-2.execute-api
- com.amazonaws.us-east-2.ssm
- com.amazonaws.us-east-2.ec2messages # Might not require this
- com.amazonaws.us-east-2.ssmmessages 

2-Launch an instance in Public Subnet With Amazon Linux 2 Image and Setup Nginx proxy with https://www.baeldung.com/nginx-forward-proxy.

3-Setup API on Nginx server with https://towardsdev.com/run-your-first-restful-api-service-using-docker-b6d8801af255

4-Create A Private REST API with proxy resource and point to Lambda with lambda proxy integration

5-Make some requests to our API like this:


- curl  https://wbtmdjhix5.execute-api.us-east-2.amazonaws.com/test/api/api/todos
- curl  https://wbtmdjhix5.execute-api.us-east-2.amazonaws.com/test/api/api/todos/1
- curl  https://wbtmdjhix5.execute-api.us-east-2.amazonaws.com/test/api/health
- curl -X POST -d '{"title": "New ToDo","description": "Testing"}' https://wbtmdjhix5.execute-api.us-east-2.amazonaws.com/test/api/api/todos

and check Nginx access logs
