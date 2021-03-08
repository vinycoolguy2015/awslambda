data "aws_availability_zones" "available" {}

data "aws_subnet_ids" "selected" {
  vpc_id     = var.vpc_id
  count      = length(local.subnet_association)
  depends_on = [aws_subnet.subnet]
  filter {
    name   = "tag:Name"
    values = [join("_", [var.vpc_name, local.subnet_association[count.index]["subnet"]])]
  }
}

resource "random_shuffle" "public_az" {
  input        = data.aws_availability_zones.available.names
  result_count = var.subnet_count
}


resource "aws_subnet" "subnet" {
  count                   = var.subnet_count
  vpc_id                  = var.vpc_id
  cidr_block              = local.subnet_association[count.index]["cidr"]
  map_public_ip_on_launch = false
  availability_zone       = random_shuffle.public_az.result[count.index]
  tags = {
    Name = join("_", [var.vpc_name, local.subnet_association[count.index]["subnet"]])
  }
  lifecycle {
    ignore_changes = [availability_zone, cidr_block, tags]
  }
}

resource "aws_route_table" "route_table" {
  vpc_id   = var.vpc_id
  for_each = var.subnets
  dynamic "route" {
    for_each = each.value.routes
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
    Name = join("_", [var.vpc_name, each.key, "route_table"])
  }
}

resource "aws_route_table_association" "route_table_association" {
  count          = var.subnet_count
  subnet_id      = distinct(flatten(local.subnet_list))[count.index].subnet_id
  route_table_id = distinct(flatten(local.subnet_list))[count.index].route_table
  lifecycle {
    ignore_changes = [subnet_id, route_table_id]
  }
}

resource "aws_network_acl" "network_acl" {
  vpc_id     = var.vpc_id
  for_each   = var.subnets
  subnet_ids = lookup(local.subnet_map, join("_", [var.vpc_name, each.key]))
  dynamic "ingress" {
    for_each = each.value.nacl_rules.ingress
    content {
      protocol   = ingress.value.protocol
      rule_no    = ingress.value.rule_no
      action     = ingress.value.action
      cidr_block = ingress.value.cidr_block
      from_port  = ingress.value.from_port
      to_port    = ingress.value.to_port
    }
  }

  dynamic "egress" {
    for_each = each.value.nacl_rules.egress
    content {
      protocol   = egress.value.protocol
      rule_no    = egress.value.rule_no
      action     = egress.value.action
      cidr_block = egress.value.cidr_block
      from_port  = egress.value.from_port
      to_port    = egress.value.to_port
    }
  }

  tags = {
    Name = join("_", [var.vpc_name, each.key, "nacl"])
  }
}