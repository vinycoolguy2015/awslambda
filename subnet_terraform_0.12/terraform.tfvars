vpc_cidr     = "10.124.0.0/16"
vpc_id       = "vpc-04de"
vpc_name     = "mtc_vpc-7"
subnet_count = 6
subnets = {
  management = {
    count   = 2
    newbits = 10
    netnum  = 0
    routes = [
      {
        cidr_block = "20.0.1.0/24"
        gateway_id = "igw-00cc81e"
      }
    ]
    nacl_rules = {
      ingress = {

        ssh_inbound = {
          from_port  = 22
          to_port    = 22
          protocol   = "tcp"
          action     = "allow"
          rule_no    = 200
          cidr_block = "20.0.0.0/24"
        },
        http_inbound = {
          from_port  = 80
          to_port    = 80
          protocol   = "tcp"
          action     = "allow"
          rule_no    = 300
          cidr_block = "20.0.0.0/24"
        }
      }

      egress = {

        ssh_outbound = {
          from_port  = 22
          to_port    = 22
          protocol   = "tcp"
          action     = "allow"
          rule_no    = 400
          cidr_block = "20.0.0.0/24"
        }
      }
    }

  }
  devops = {
    newbits = 10
    count   = 2
    netnum  = 4
    routes = [
      {
        cidr_block = "20.0.1.0/24"
        gateway_id = "igw-00cc81e"
      },
      {
        cidr_block = "30.0.1.0/24"
        gateway_id = "igw-00cc81e"
      }
    ]
    nacl_rules = {
      ingress = {

        ssh_inbound = {
          from_port  = 22
          to_port    = 22
          protocol   = "tcp"
          action     = "allow"
          rule_no    = 200
          cidr_block = "20.0.0.0/24"
        }
      }

      egress = {

        ssh_outbound = {
          from_port  = 22
          to_port    = 22
          protocol   = "tcp"
          action     = "allow"
          rule_no    = 400
          cidr_block = "20.0.0.0/24"
        }
      }

    }
  }
  endpoints = {
    newbits = 10
    netnum  = 8
    count   = 2
    routes = [
      {
        cidr_block = "30.0.1.0/24"
        gateway_id = "igw-00cc81"
      }
    ]
    nacl_rules = {

      ingress = {

        ssh_inbound = {
          from_port  = 22
          to_port    = 22
          protocol   = "tcp"
          action     = "allow"
          rule_no    = 300
          cidr_block = "20.0.0.0/24"
        }
      }

      egress = {

        ssh_outbound = {
          from_port  = 22
          to_port    = 22
          protocol   = "tcp"
          action     = "allow"
          rule_no    = 400
          cidr_block = "20.0.0.0/24"
        }
      }

    }
  }
}
