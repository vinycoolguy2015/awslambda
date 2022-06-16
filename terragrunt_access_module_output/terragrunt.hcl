generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite"
  contents = <<EOF
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "3.7"
    }
  }
  backend "s3" {}
}
provider "aws" {
  region              = "us-east-1"
}
EOF
}


# Remote backend settings for all child directories
remote_state {
  backend = "s3"
  config = {
    bucket         = "ca-tf-state-${get_aws_account_id()}"
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
