vpc_id = "vpc-04dee5eb35504d726"
security_groups = {
  security_group1 = {
    name        = "security_group1"
    description = "Initial security group"
    rules = {
      ingress = {
        ssh_inbound = {
          description = "Allow SSH"
          from_port   = 22
          to_port     = 22
          protocol    = "tcp"
          cidr_blocks = ["20.0.0.0/24", "200.0.0.0/24"]
        },
        http_inbound = {
          description = "Allow HTTP from CIDR"
          from_port   = 80
          to_port     = 80
          protocol    = "tcp"
          cidr_blocks = ["20.0.0.0/24", "200.0.0.0/24"]
        }
        http_inbound2 = {
          description     = "Allow HTTP from SG"
          from_port       = 80
          to_port         = 80
          protocol        = "tcp"
          security_groups = ["sg-030323d812f0a9e9b"]
        }
      }
      egress = {
        default = {
          description = "Default egress"
          from_port   = 0
          to_port     = 0
          protocol    = "-1"
          cidr_blocks = ["0.0.0.0/0"]
        }
      }
    }
  },
  security_group2 = {
    name        = "security_group2"
    description = "Second security group"
    rules = {
      ingress = {
        ssh_inbound = {
          description = "Allow SSH"
          from_port   = 22
          to_port     = 22
          protocol    = "tcp"
          cidr_blocks = ["20.0.0.0/24", "200.0.0.0/24"]
        },
        http_inbound = {
          description = "Allow HTTP from CIDR"
          from_port   = 80
          to_port     = 80
          protocol    = "tcp"
          cidr_blocks = ["20.0.0.0/24", "100.0.0.0/24"]
        }
        http_inbound2 = {
          description     = "Allow HTTP from SG"
          from_port       = 80
          to_port         = 80
          protocol        = "tcp"
          security_groups = ["sg-030323d812f0a9e9b"]
        }
      }
      egress = {
        default = {
          description = "Default egress"
          from_port   = 0
          to_port     = 0
          protocol    = "-1"
          cidr_blocks = ["0.0.0.0/0"]
        }
      }
    }

  }
}