aws_profile         = "default"
aws_region          = "us-east-1"
key_name            = "kp_devops"
vpc_name            = "vpc_devops"
public_subnet_name  = "sub_public_devops"
security_group_name = "sg_devops"
public_key_path     = "~/.ssh/id_rsa.pub"
instance_type       = "t2.micro"
instance_name       = "ec2_devops"
instance_ami        = "ami-b73b63a0"
cidrs = {
  vpc          = "10.0.0.0/16"
  publicsubnet = "10.0.0.0/24"
}
