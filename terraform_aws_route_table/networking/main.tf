data "aws_availability_zones" "available" {}


resource "random_integer" "random" {
  min = 1
  max = 100
}

resource "random_shuffle" "public_az" {
  input        = data.aws_availability_zones.available.names
  result_count = var.private_sn_count
}

resource "aws_vpc" "test_vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "test_vpc-${random_integer.random.id}"
  }
  lifecycle {
    create_before_destroy = true
  }
}


resource "aws_subnet" "test_private_subnet" {
  count                   = var.private_sn_count
  vpc_id                  = aws_vpc.test_vpc.id
  cidr_block              = var.private_cidrs[count.index]
  map_public_ip_on_launch = false
  availability_zone       = random_shuffle.public_az.result[count.index]

  tags = {
    Name = "test_private_${count.index + 1}"
  }
  lifecycle {
    ignore_changes = [availability_zone]
  }
}

resource "aws_default_route_table" "test_private_rt" {
  default_route_table_id = aws_vpc.test_vpc.default_route_table_id

  tags = {
    Name = "test_private"
  }
}

resource "aws_route" "aws_route_gateway" {
  route_table_id         = aws_vpc.test_vpc.default_route_table_id
  for_each               = var.create_gateway_routes ? var.routes.gateway : {}
  destination_cidr_block = each.key
  gateway_id             = each.value
}

resource "aws_route" "aws_route_peering" {
  route_table_id            = aws_vpc.test_vpc.default_route_table_id
  for_each                  = var.create_peering_routes ? var.routes.peering : {}
  destination_cidr_block    = each.key
  vpc_peering_connection_id = each.value
}

resource "aws_route" "aws_route_nat" {
  route_table_id         = aws_vpc.test_vpc.default_route_table_id
  for_each               = var.create_nat_routes ? var.routes.nat_gateway : {}
  destination_cidr_block = each.key
  nat_gateway_id         = each.value
}

resource "aws_default_network_acl" "default" {
  default_network_acl_id = aws_vpc.test_vpc.default_network_acl_id

  ingress {
    protocol   = -1
    rule_no    = 100
    action     = "allow"
    cidr_block = aws_vpc.test_vpc.cidr_block
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
}

resource "aws_network_acl_rule" "nacl_rules" {
  network_acl_id = aws_vpc.test_vpc.default_network_acl_id
  for_each       = var.create_nacl_rules ? var.nacl_rules.private : {}
  rule_action    = each.value.rule_action
  rule_number    = each.value.rule_number
  from_port      = each.value.from_port
  to_port        = each.value.to_port
  protocol       = each.value.protocol
  cidr_block     = each.value.cidr_block
  egress         = each.value.egress

}

