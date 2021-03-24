provider "aws" {
  region = var.aws_region
}

data "aws_availability_zones" "available" {
}

# VPC
resource "aws_vpc" "vpc" {
  cidr_block = var.cidrs["vpc"]
  tags = {
    Name = var.vpc_name
  }
}

#internet gateway

resource "aws_internet_gateway" "internet_gateway" {
  vpc_id = aws_vpc.vpc.id
}

# Route tables

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.internet_gateway.id
  }

  tags = {
    Name = "public"
  }
}

resource "aws_default_route_table" "private" {
  default_route_table_id = aws_vpc.vpc.default_route_table_id

  tags = {
    Name = "private"
  }
}

resource "aws_subnet" "public1" {
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = var.cidrs["publicsubnet"]
  map_public_ip_on_launch = true
  availability_zone       = data.aws_availability_zones.available.names[0]

  tags = {
    Name = var.public_subnet_name
  }
}

# Subnet Associations

resource "aws_route_table_association" "public1_assoc" {
  subnet_id      = aws_subnet.public1.id
  route_table_id = aws_route_table.public.id
}

resource "aws_security_group" "instance_sg" {
  name = var.security_group_name

  #description = "EC2 instance security group"
  vpc_id = aws_vpc.vpc.id

  #SSH

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  #HTTP

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  #Tomcat
  
  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  #Outbound internet access

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# key pair

resource "aws_key_pair" "auth" {
  key_name   = var.key_name
  public_key = file(var.public_key_path)
}

# server

resource "aws_instance" "instance" {
  instance_type = var.instance_type
  ami           = var.instance_ami

  tags = {
    Name = var.instance_name
  }

  key_name               = aws_key_pair.auth.id
  vpc_security_group_ids = [aws_security_group.instance_sg.id]
  subnet_id              = aws_subnet.public1.id

  provisioner "local-exec" {
    command = <<EOD
cat <<EOF > aws_hosts
[ec2]
${aws_instance.instance.public_ip}
EOF
EOD

  }

  provisioner "local-exec" {
    command = "aws ec2 wait instance-status-ok --instance-ids ${aws_instance.instance.id} && ansible-playbook -i aws_hosts script.yaml"
  }
}

resource "aws_eip" "instance" {
  vpc = true
}

resource "aws_eip_association" "eip_assoc" {
  instance_id   = aws_instance.instance.id
  allocation_id = aws_eip.instance.id
}

#-------OUTPUTS ------------

output "instance_ip_address" {
  value = aws_eip.instance.public_ip
}

