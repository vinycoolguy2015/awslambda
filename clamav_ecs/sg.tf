resource "aws_security_group" "clamav-sg" {
  name        = "sgrp-clamav"
  description = "Security group for Clamav"
  vpc_id      = var.vpc_id
}

#resource "aws_security_group_rule" "clamav-sg-egress" {
#  type        = "egress"
#  description = "Security Group for Clamav"
#  from_port   = 443
#  to_port     = 443
#  protocol    = "tcp"
#  cidr_blocks       = ["0.0.0.0/0"]
#  security_group_id = aws_security_group.clamav-sg.id
#}

resource "aws_security_group_rule" "clamav-sg-ingress" {
  type                     = "ingress"
  description              = "Security Group for Clamav"
  from_port                = 8080
  to_port                  = 8080
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.lb-sg.id
  security_group_id        = aws_security_group.clamav-sg.id
}

resource "aws_security_group" "lb-sg" {
  name        = "sgrp-clamav-lb"
  description = "Security group for Clamav LB"
  vpc_id      = var.vpc_id
}

resource "aws_security_group_rule" "lb-egress-sg" {
  type                     = "egress"
  description              = "Security Group for LB"
  from_port                = 8080
  to_port                  = 8080
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.clamav-sg.id
  security_group_id        = aws_security_group.lb-sg.id
}

resource "aws_security_group_rule" "lb-ingress-sg" {
  type                     = "ingress"
  description              = "Security Group for LB"
  from_port                = 80
  to_port                  = 80
  protocol                 = "tcp"
  cidr_blocks              = ["0.0.0.0/0"]
  security_group_id        = aws_security_group.lb-sg.id
}

resource "aws_security_group" "app-sg" {
  name        = "sgrp-clamav-app"
  description = "Security group for App"
  vpc_id      = var.vpc_id
}

resource "aws_security_group_rule" "app-sg" {
  type                     = "egress"
  description              = "Security Group for App"
  from_port                = 80
  to_port                  = 80
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.lb-sg.id
  security_group_id        = aws_security_group.app-sg.id
}
