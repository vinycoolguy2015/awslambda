terraform {
  backend "s3" {}
}

provider "aws" {
  region = "ap-southeast-1"
}
