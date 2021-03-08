locals {

  expanded_subnets = {
    for key, value in var.subnets :
    key => [
    for i in range(value.count) : format("%s", cidrsubnet(var.vpc_cidr, value.newbits, value.netnum + i))]
  }

  subnet_association = flatten([
    for subnet in keys(local.expanded_subnets) : [
      for cidr in local.expanded_subnets[subnet] : {
        subnet      = subnet
        cidr        = cidr
        route_table = aws_route_table.route_table[subnet].id

      }
    ]
  ])


  subnet_split = [for subnet in distinct(data.aws_subnet_ids.selected) : [
    for id in subnet.ids : {
      id           = id
      subnet_split = split("_", join("", flatten(subnet.filter)[0].values))

    }
    ]
  ]


  subnet_parse = [for subnet in flatten(local.subnet_split) : {
    id     = subnet.id
    subnet = slice(subnet.subnet_split, length(subnet.subnet_split) - 1, length(subnet.subnet_split))[0]

    }
  ]

  subnet_list = [
    for subnet in local.subnet_association : [
      for subnet_id in local.subnet_parse :
      {

        route_table = subnet.route_table
        subnet      = subnet.subnet
        subnet_id   = subnet_id.id
      }
      if subnet_id.subnet == subnet.subnet
    ]
  ]

  subnet_map = zipmap(flatten(flatten(distinct(data.aws_subnet_ids.selected))[*].filter.*.values[0]), flatten(distinct(data.aws_subnet_ids.selected))[*].ids)

}

