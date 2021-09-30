variable "region" {
  default = "us-east-1"
}
variable "ecs_service_name" {}
variable "docker_image_url" {}
variable "memory" {}
variable "docker_container_port" {}
variable "desired_task_number" {}
variable "message" {}
variable "private_subnets" {}
variable "ecs_security_group" {}
variable "target_group_arn" {}
variable "ecs_cluster_name" {}
variable "execution_role_arn" {}
variable "task_role_arn" {}
variable "cpu" {}
