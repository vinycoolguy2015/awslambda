resource "aws_security_group" "gateway_endpoint_sg" {
  name        = "gateway_endpoint_sg"
  description = "Allow HTTPS inbound traffic"
  vpc_id      = var.vpc_id

  ingress {
    description = "HTTPS from VPC"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr_block]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "gateway_endpoint_sg"
  }
}

resource "aws_vpc_endpoint" "api_gateway_endpoint" {
  vpc_id              = var.vpc_id
  service_name        = "com.amazonaws.${data.aws_region.current.name}.execute-api"
  private_dns_enabled = true
  subnet_ids          = [var.subnet_id]
  security_group_ids  = [aws_security_group.gateway_endpoint_sg.id]
  vpc_endpoint_type   = "Interface"
  tags = {
    Name = "api_gateway_endpoint"
  }
}

