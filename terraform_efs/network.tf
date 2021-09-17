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
