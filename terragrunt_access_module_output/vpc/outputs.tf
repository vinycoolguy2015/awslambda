output "vpc_id" {
    description = "ID of the VPC"
    value = aws_vpc.prod.id
}

output "vpc_sg" {
    description = "Default security group of the VPC"
    value = aws_vpc.prod.default_security_group_id 
}
