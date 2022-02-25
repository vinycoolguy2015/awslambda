variable "env_name" {}
variable "repo_name" {}
variable "main_listener" {}
variable "main_target_group" {}
variable "test_target_group" {}
variable "test_listener" {}
variable "ecs_service_name" {}
variable "ecs_cluster_name" {}
variable "termination_wait_time_in_minutes" {}
variable "deployment_config_name" { default = "CodeDeployDefault.ECSAllAtOnce" }
variable "ecr_repository_name" {}
