vpc_id              = "vpc-04dee5eb35504d726"
security_group_name = "test"
description         = "test"

security_group_rules = {

  ssh_inbound = {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    type        = "ingress"
    cidr_blocks = ["10.0.0.0/24", "10.0.1.0/24"]
    description = "Allow inbound SSH access"
  }
  ssh_inbound2 = {
    from_port      = 22
    to_port        = 22
    protocol       = "tcp"
    type           = "ingress"
    security_group = "sg-030323d812f0a9e9b"
    description    = "Allow inbound SSH access"
  }
  http_inbound = {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    type        = "ingress"
    cidr_blocks = ["10.0.0.0/24"]
    description = "Allow inbound HTTP access"
  }
  ssh_outbound = {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    type        = "egress"
    cidr_blocks = ["10.0.0.0/24"]
    description = "Allow outbound SSH access"
  }
  http_outbound = {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    type        = "egress"
    cidr_blocks = ["10.0.0.0/24"]
    description = "Allow outbound HTTP access"

  }
}