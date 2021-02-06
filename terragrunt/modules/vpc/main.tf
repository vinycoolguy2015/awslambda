data "aws_availability_zones" "available" {}

#--------------------------------------------------------------------- Create VPC

resource "aws_vpc" "vpc" {
  cidr_block = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags = {
    Name = "Application_VPC"
  }
}


#--------------------------------------------------------------------- Create Internet Gateway

#internet gateway

resource "aws_internet_gateway" "internet_gateway" {
  vpc_id = aws_vpc.vpc.id
  tags = {
    Name = "Application_VPC_Internet_Gateway"
  }
}


#--------------------------------------------------------------------- Create Route Table

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

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.vpc_nat_gateway.id
  }

  tags = {
    Name = "Private Route Table"
  }

  depends_on = [aws_nat_gateway.vpc_nat_gateway]
}


#--------------------------------------------------------------Create Public and Private Subnets

resource "aws_subnet" "vpc_public_subnet" {
  count                   = var.subnet_count
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = var.vpc_public_subnet_cidrs[count.index]
  map_public_ip_on_launch = true
  availability_zone       = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "VPC_Public_Subnet_${count.index + 1}"
  }
}

resource "aws_subnet" "vpc_private_subnet" {
  count                   = var.subnet_count
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = var.vpc_private_subnet_cidrs[count.index]
  map_public_ip_on_launch = false
  availability_zone       = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "VPC_Private_Subnet_${count.index + 1}"
  }
}


#--------------------------------------------------------------------- Create NAT Gateway

resource "aws_eip" "vpc_nat_gateway_eip" {
  vpc = true
}

resource "aws_nat_gateway" "vpc_nat_gateway" {
  allocation_id = aws_eip.vpc_nat_gateway_eip.id
  subnet_id     = aws_subnet.vpc_public_subnet.*.id[0]
  tags = {
    Name = "Application VPC Nat Gateway"
  }
}

#--------------------------------------------------------------------- Create Route Table association


resource "aws_route_table_association" "vpc_public_assoc" {
  count          = var.subnet_count
  subnet_id      = aws_subnet.vpc_public_subnet.*.id[count.index]
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "vpc_private_assoc" {
  count          = var.subnet_count
  subnet_id      = aws_subnet.vpc_private_subnet.*.id[count.index]
  route_table_id = aws_route_table.private.id
}



#--------------------------------------------------------------------- Create DB Subnet Group
resource "aws_db_subnet_group" "rds_subnetgroup" {
  name       = "rds_subnetgroup"
  subnet_ids = ["${aws_subnet.vpc_private_subnet.*.id[0]}","${aws_subnet.vpc_private_subnet.*.id[1]}"]

  tags = {
    Name = "RDS_Subnet_Group"
  }
}


#--------------------------------------------------------------------- Create Security Group

resource "aws_security_group" "instance_sg" {
  name        = "Instance_Security_Group"
  description = "Web Server Security Group"
  vpc_id      = aws_vpc.vpc.id
  ingress {
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    security_groups = ["${aws_security_group.alb_sg.id}"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "alb_sg" {
  name        = "ALB_Security Group"
  description = "Application Load Balancer Security Group"
  vpc_id      = aws_vpc.vpc.id
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_security_group" "rds_sg" {
  name        = "RDS_Security_Group"
  description = "RDS Instance Security Group"
  vpc_id      = aws_vpc.vpc.id
  ingress {
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = ["${aws_security_group.instance_sg.id}"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
