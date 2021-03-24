data "aws_availability_zones" "available" {}

#--------------------------------------------------------------------- Create VPC

resource "aws_vpc" "vpc" {
  cidr_block           = var.vpc_cidr
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
  subnet_ids = [aws_subnet.vpc_private_subnet.*.id[0], aws_subnet.vpc_private_subnet.*.id[1]]

  tags = {
    Name = "RDS_Subnet_Group"
  }
}


