data "aws_availability_zones" "available" {}

resource "aws_vpc" "vpc" {
   cidr_block = "10.0.0.0/16"
   enable_dns_hostnames = true
   enable_dns_support = true
   tags= {
     Name = "test-env"
   }
 }

resource "aws_internet_gateway" "internet_gateway" {
  vpc_id = aws_vpc.vpc.id
  tags = {
    Name = "Internet_Gateway"
  }
}
 
 resource "aws_subnet" "subnet" {
   count=length(data.aws_availability_zones.available.names)
   cidr_block = cidrsubnet(aws_vpc.vpc.cidr_block, 8, count.index)
   vpc_id = aws_vpc.vpc.id
   availability_zone = data.aws_availability_zones.available.names[count.index]
 }


resource "aws_route_table" "public" {
  vpc_id = aws_vpc.vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.internet_gateway.id
  }

  tags = {
    Name = "Public Route Table"
  }
  depends_on = [aws_internet_gateway.internet_gateway]
}

resource "aws_route_table_association" "vpc_public_assoc" {
  count          = length(data.aws_availability_zones.available.names)
  subnet_id      = aws_subnet.subnet.*.id[count.index]
  route_table_id = aws_route_table.public.id
}

resource "aws_kms_key" "efs" {
  count = var.env == "prod" || var.env == "stag" ? 1 : 0
  description             = "KMS"
  deletion_window_in_days = 7
}

resource "aws_security_group" "ec2" {
  name        = "allow_efs"
  description = "Allow efs outbound traffic"
  vpc_id      = aws_vpc.vpc.id
  ingress {
     cidr_blocks = ["0.0.0.0/0"]
     from_port = 22
     to_port = 22
     protocol = "tcp"
   }
  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["0.0.0.0/0"]
  }
  tags = {
    Name = "allow_efs"
  }
}

resource "aws_security_group" "efs" {
   name = "efs-sg"
   description= "Allos inbound efs traffic from ec2"
   vpc_id = aws_vpc.vpc.id

   ingress {
     security_groups = [aws_security_group.ec2.id]
     from_port = 2049
     to_port = 2049 
     protocol = "tcp"
   }     
        
   egress {
     security_groups = [aws_security_group.ec2.id]
     from_port = 0
     to_port = 0
     protocol = "-1"
   }
 }

resource "aws_efs_file_system" "efs" {
   creation_token = "efs"
   performance_mode = "generalPurpose"
   throughput_mode = "bursting"
   encrypted = "true"
   kms_key_id= var.env != "prod" && var.env != "stag" ? null : aws_kms_key.efs[0].arn
 tags = {
     Name = "EFS"
   }
 }


resource "aws_efs_mount_target" "efs-mt" {
   count = length(data.aws_availability_zones.available.names)
   file_system_id  = aws_efs_file_system.efs.id
   subnet_id = aws_subnet.subnet[count.index].id
   security_groups = [aws_security_group.efs.id]
 }
