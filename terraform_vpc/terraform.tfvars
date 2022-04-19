vpc_cidr          = "10.6.0.0/16"
private_subnet = { count = 3, newbits = 8, netnum = 0 }
public_subnet     = { count = 3, newbits = 8, netnum = 4 }


