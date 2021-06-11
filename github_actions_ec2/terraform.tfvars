subnet_count             = "2"
vpc_cidr                 = "10.1.0.0/16"
vpc_public_subnet_cidrs  = ["10.1.0.0/24", "10.1.1.0/24"]
vpc_private_subnet_cidrs = ["10.1.2.0/24", "10.1.3.0/24"]
aws_region               = "us-east-1"
ami                      = "ami-0aeeebd8d2ab47354"
public_key_path          = "~/.ssh/id_rsa.pub"
instance_type            = "t2.micro"
highcpu                  = 75
lowcpu                   = 40
userdata                 = "script.tpl"
environments = {
  environment1 = "Dev"
}
