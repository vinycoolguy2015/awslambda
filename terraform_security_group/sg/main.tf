resource "aws_security_group" "security_group" {
  name        = var.security_group_name
  description = var.description
  vpc_id      = var.vpc_id
  tags = {
    Name = var.security_group_name
  }
}

resource "aws_security_group_rule" "allow_self_ingress" {
  type                     = "ingress"
  from_port                = 0
  to_port                  = 65535
  protocol                 = "-1"
  security_group_id        = aws_security_group.security_group.id
  source_security_group_id = aws_security_group.security_group.id
}

resource "aws_security_group_rule" "allow_default_egress" {
  type              = "egress"
  from_port         = 0
  to_port           = 65535
  protocol          = "-1"
  security_group_id = aws_security_group.security_group.id
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "sg_rules" {
  for_each                 = var.security_group_rules
  type                     = each.value.type
  from_port                = each.value.from_port
  to_port                  = each.value.to_port
  protocol                 = each.value.protocol
  cidr_blocks              = lookup(each.value, "cidr_blocks", null)
  security_group_id        = aws_security_group.security_group.id
  source_security_group_id = lookup(each.value, "security_group", null)
}