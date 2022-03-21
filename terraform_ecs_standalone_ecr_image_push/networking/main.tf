data "aws_availability_zones" "available" {}

resource "random_shuffle" "public_az" {
  input        = data.aws_availability_zones.available.names
  result_count = 10
}

resource "aws_vpc" "vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = var.vpc_name
  }
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_internet_gateway" "internet_gateway" {
  vpc_id = aws_vpc.vpc.id
  tags = {
    Name = join("_", [var.vpc_name, "internet_gateway"])
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.internet_gateway.id
  }

  tags = {
    Name = join("_", [var.vpc_name, "public_route_table"])
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
    Name = join("_", [var.vpc_name, "private_route_table"])
  }

  depends_on = [aws_nat_gateway.vpc_nat_gateway]
}

resource "aws_subnet" "public_subnet" {
  count                   = var.public_subnet["count"]
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = cidrsubnet(var.vpc_cidr, var.public_subnet["newbits"], var.public_subnet["netnum"] + count.index)
  map_public_ip_on_launch = true
  availability_zone       = random_shuffle.public_az.result[count.index]

  tags = {
    Name = join("_", [var.vpc_name, "public_subnet", count.index + 1])
  }
  lifecycle {
    ignore_changes = [availability_zone]
  }
}

resource "aws_subnet" "private_subnet" {
  count                   = var.private_subnet["count"]
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = cidrsubnet(var.vpc_cidr, var.private_subnet["newbits"], var.private_subnet["netnum"] + count.index)
  map_public_ip_on_launch = false
  availability_zone       = random_shuffle.public_az.result[count.index]

  tags = {
    Name = join("_", [var.vpc_name, "private_subnet", count.index + 1])
  }
  lifecycle {
    ignore_changes = [availability_zone]
  }
}

resource "aws_eip" "vpc_nat_gateway_eip" {
  vpc = true
}

resource "aws_nat_gateway" "vpc_nat_gateway" {
  allocation_id = aws_eip.vpc_nat_gateway_eip.id
  subnet_id     = aws_subnet.public_subnet.*.id[0]
  tags = {
    Name = join("_", [var.vpc_name, "nat_gateway"])
  }
}

resource "aws_route_table_association" "vpc_public_assoc" {
  count          = var.public_subnet["count"]
  subnet_id      = aws_subnet.public_subnet.*.id[count.index]
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "vpc_private_assoc" {
  count          = var.private_subnet["count"]
  subnet_id      = aws_subnet.private_subnet.*.id[count.index]
  route_table_id = aws_route_table.private.id
}


resource "aws_default_network_acl" "default" {
  default_network_acl_id = aws_vpc.vpc.default_network_acl_id

  ingress {
    protocol   = -1
    rule_no    = 100
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 0
    to_port    = 0
  }

  egress {
    protocol   = -1
    rule_no    = 100
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 0
    to_port    = 0
  }


  lifecycle {
    ignore_changes = [subnet_ids]
  }

  tags = {
    Name = join("_", [var.vpc_name, "default_nacl"])
  }
}


