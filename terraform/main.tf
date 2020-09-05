provider "aws" {
  region = "us-east-1"
}

module "keypair" {
  source       = "jangjaelee/keypair/aws"
  version      = "0.1.0"
  keypair_file = "/Users/viny/.ssh/id_rsa.pub"
  keypair_name = "web"
}

module "vpc" {
  source             = "terraform-aws-modules/vpc/aws"
  name               = "custom-vpc"
  cidr               = "10.0.0.0/16"
  azs                = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets    = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets     = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
  enable_nat_gateway = true
  tags = {
    Terraform   = "true"
    Environment = "dev"
  }
}

module "web_server_sg" {
  source              = "terraform-aws-modules/security-group/aws"
  name                = "web-server"
  description         = "Security group for web-server"
  vpc_id              = module.vpc.vpc_id
  ingress_cidr_blocks = ["0.0.0.0/0"]
  ingress_rules       = ["http-80-tcp"]
}

module "asg" {
  source  = "terraform-aws-modules/autoscaling/aws"
  version = "~> 3.0"
  name    = "web-server"
  # Launch configuration
  lc_name = "web-server-lc"

  image_id        = "ami-06b263d6ceff0b3dd"
  instance_type   = "t2.micro"
  key_name        = module.keypair.info-keypair-name
  user_data       = file("script.sh")
  security_groups = [module.web_server_sg.this_security_group_id]
  root_block_device = [
    {
      volume_size = "10"
      volume_type = "gp2"
    },
  ]
  # Auto scaling group
  asg_name                  = "web-server-asg"
  vpc_zone_identifier       = module.vpc.public_subnets
  health_check_type         = "EC2"
  min_size                  = 0
  max_size                  = 1
  desired_capacity          = 1
  wait_for_capacity_timeout = 0
  tags = [
    {
      key                 = "Environment"
      value               = "dev"
      propagate_at_launch = true
    }
  ]
}
