data "terraform_remote_state" "vpc" {
  backend = "s3"
  config = {
    region = "us-east-1"
    bucket = "my-terraform-state-1989"
    key    = "web_application/vpc/terraform.tfstate"
  }
}
