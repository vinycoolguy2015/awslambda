resource "aws_security_group" "security_group" {
  for_each    = var.security_groups
  name        = each.value.name
  description = each.value.description
  vpc_id      = var.vpc_id

  ingress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    description = "Allow access from self"
    self        = true
  }

  dynamic "ingress" {
    for_each = each.value.rules.ingress
    content {
      protocol        = ingress.value.protocol
      cidr_blocks     = lookup(ingress.value, "cidr_blocks", null)
      security_groups = lookup(ingress.value, "security_groups", null)
      from_port       = ingress.value.from_port
      to_port         = ingress.value.to_port
      description     = ingress.value.description
    }
  }

  dynamic "egress" {
    for_each = each.value.rules.egress
    content {
      protocol        = egress.value.protocol
      cidr_blocks     = lookup(egress.value, "cidr_blocks", null)
      security_groups = lookup(egress.value, "security_groups", null)
      from_port       = egress.value.from_port
      to_port         = egress.value.to_port
      description     = egress.value.description
    }
  }

  tags = {
    Name = each.value.name
  }
}