output "vpc_id" {
  value = "${aws_vpc.vpc.id}"
}

output "vpc_public_subnets" {
  value = "${aws_subnet.vpc_public_subnet.*.id}"
}

output "vpc_private_subnets" {
  value = "${aws_subnet.vpc_private_subnet.*.id}"
}

output "rds_subnetgroup" {
  value = "${aws_db_subnet_group.rds_subnetgroup.name}"
}

output "instance_security_group" {
  value= "${aws_security_group.instance_sg.id}"
}
 
output "lb_security_group" {
  value= "${aws_security_group.alb_sg.id}"
}

output "rds_security_group" {
  value= "${aws_security_group.rds_sg.id}"
}

