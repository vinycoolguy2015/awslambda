variable "region" {
  default = "us-east-1"
}
variable "ecs_cluster_name" {}
variable "execution_role_arn" {}
variable "task_role_arn" {}
variable "private_subnets" {}
variable "ecs_security_group" {}
variable "target_group_arn" {}
variable "docker_container_port" {}
variable "vpc_id" {}
