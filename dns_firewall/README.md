Can also search VPC with a Tag and process it like this if multiple VPCs returned by the data source

```
data "aws_vpcs" "vpc" {
  filter {
    name   = "tag:Environment"
    values = [var.tags["Environment"]]
  }
}


resource "aws_route53_resolver_firewall_config" "dns_firewall" {
  for_each           = toset(data.aws_vpcs.vpc.ids)
  resource_id        = each.key
  firewall_fail_open = "ENABLED"
}
````
