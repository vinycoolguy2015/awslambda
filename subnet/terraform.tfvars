vpc_cidr = "10.124.0.0/16"
vpc_id   = "vpc-04dee"
vpc_name = "test"

subnets = {
  management_subnet = {
    count   = 2
    newbits = 10
    netnum  = 0

    routes = [
      {
        cidr_block = "10.0.1.0/24"
        gateway_id = "igw-00cc81e0"
      }
    ]

    nacl_rules = {
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
        cidr_block  = "20.0.0.0/24"
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
  devops_subnet = {
    count   = 2
    newbits = 10
    netnum  = 4
    routes = [
      {
        cidr_block = "20.0.1.0/24"
        gateway_id = "igw-00cc81e03e"
      }
    ]
    nacl_rules = {

      ssh_inbound = {
        from_port   = 22
        to_port     = 22
        protocol    = "tcp"
        rule_action = "allow"
        rule_number = 200
        egress      = false
        cidr_block  = "20.0.0.0/24"
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
        cidr_block  = "20.0.0.0/24"
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
  endpoints_subnet = {
    count   = 2
    newbits = 10
    netnum  = 8
    routes = [
      {
        cidr_block = "30.0.1.0/24"
        gateway_id = "igw-00cc81e03e"
      }
    ]
    nacl_rules = {

      ssh_inbound = {
        from_port   = 22
        to_port     = 22
        protocol    = "tcp"
        rule_action = "allow"
        rule_number = 200
        egress      = false
        cidr_block  = "30.0.0.0/24"
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
        cidr_block  = "30.0.0.0/24"
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
}




