vpc_cidr          = "10.6.0.0/16"
management_subnet = { count = 2, newbits = 10, netnum = 0 }
devops_subnet     = { count = 2, newbits = 10, netnum = 4 }
endpoints_subnet  = { count = 2, newbits = 10, netnum = 8 }


routes = {
  gateway = {
    "10.0.0.0/24" = "igw-099284ce90058eb76"
    "20.0.0.0/24" = "igw-099284ce90058eb76"
  }

  nat_gateway = {
    "40.0.0.0/24" = "nat-08fa74d7aad4132a7"
    "50.0.0.0/24" = "nat-08fa74d7aad4132a7"

  }
}

nacl_rules = {
  private = {
    ssh_inbound = {
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      rule_action = "allow"
      rule_number = 200
      egress      = false
      cidr_block  = "10.0.0.0/24"
    }
    http_inbound = {
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      rule_action = "allow"
      rule_number = 300
      egress      = false
      cidr_block  = "0.0.0.0/0"
    }

    ssh_outbound = {
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      rule_action = "allow"
      rule_number = 400
      egress      = true
      cidr_block  = "10.0.0.0/24"
    }
    http_outbound = {
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      rule_action = "allow"
      rule_number = 500
      egress      = true
      cidr_block  = "0.0.0.0/0"
    }
  }
}

