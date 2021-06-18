
//Deploy Application with Github repository
isECR                = false
build_command        = "npm install"
runtime              = "NODEJS_12"
start_command        = "npm run start"
configuration_source = "API"
repository_url       = "https://github.com/vinycoolguy2015/express-hello-world"
repository_branch    = "master"
port                 = "80"
connection_arn       = "arn:aws:apprunner:us-east-2:xyz:connection/node/d3351b8fa47a464987022780dccb38a4"
auto_deployments_enabled = "true" 
