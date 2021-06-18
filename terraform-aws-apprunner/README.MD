This code is not working. So create a Github connection manually and specify connection ARN in terraform.tfvars

resource "aws_apprunner_connection" "example" {
  connection_name = "example"
  provider_type = "GITHUB"
  tags = {
    Name = "example-gh-connection"
  }
}

Once service is deployed,make some changes to the source code repo and it will be auto-deployed.
