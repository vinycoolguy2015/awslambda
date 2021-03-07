#https://stackoverflow.com/questions/65334293/how-do-i-do-a-dynamic-route-in-aws-route-table

data "aws_availability_zones" "available" {}

resource "random_shuffle" "public_az" {
  input        = data.aws_availability_zones.available.names
  result_count = 10
}

resource "aws_subnet" "subnet" {
  count                   = var.subnet_count
  vpc_id                  = var.vpc_id
  cidr_block              = cidrsubnet(var.vpc_cidr, var.newbits, var.netnum + count.index)
  map_public_ip_on_launch = false
  availability_zone       = random_shuffle.public_az.result[count.index]

  tags = {
    Name = join("_", [var.vpc_name, var.subnet_name, count.index + 1])
  }
  lifecycle {
    ignore_changes = [availability_zone]
  }
}


resource "aws_route_table" "route_table" {
  vpc_id = var.vpc_id
  dynamic "route" {
    for_each = var.routes
    content {
      cidr_block         = lookup(route.value, "cidr_block", null)
      gateway_id         = lookup(route.value, "gateway_id", null)
      nat_gateway_id     = lookup(route.value, "nat_gateway_id", null)
      instance_id        = lookup(route.value, "instance_id", null)
      transit_gateway_id = lookup(route.value, "transit_gateway_id", null)
      vpc_endpoint_id    = lookup(route.value, "vpc_endpoint_id", null)

    }
  }
  tags = {
    Name = join("_", [var.vpc_name, var.subnet_name, "route_table"])
  }
}

resource "aws_route_table_association" "route_table_association" {
  count          = var.subnet_count
  subnet_id      = aws_subnet.subnet.*.id[count.index]
  route_table_id = aws_route_table.route_table.id
}

resource "aws_network_acl" "network_acl" {
  vpc_id     = var.vpc_id
  subnet_ids = aws_subnet.subnet.*.id
  tags = {
    Name = join("_", [var.vpc_name, var.subnet_name, "nacl"])
  }
}

resource "aws_network_acl_rule" "nacl_rules" {
  network_acl_id = aws_network_acl.network_acl.id
  for_each       = var.nacl_rules
  rule_action    = each.value.rule_action
  rule_number    = each.value.rule_number
  from_port      = each.value.from_port
  to_port        = each.value.to_port
  protocol       = each.value.protocol
  cidr_block     = each.value.cidr_block
  egress         = each.value.egress

}
