vpc_cidr         = "10.123.0.0/16"
private_sn_count = 4


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