output "vpc_id" {
  value = aws_vpc.vpc.id
}

output "vpc_public_subnets" {
  value = aws_subnet.vpc_public_subnet.*.id
}

output "vpc_private_subnets" {
  value = aws_subnet.vpc_private_subnet.*.id
}

output "rds_subnetgroup" {
  value = aws_db_subnet_group.rds_subnetgroup.name
}


