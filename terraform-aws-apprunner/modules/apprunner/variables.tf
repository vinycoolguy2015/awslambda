variable "region" {
  description = "The region to launch the bastion host"
}

variable "environment" {
  description = "The Deployment environment"
}

variable "random_id_prefix" {
  description = "random prefix for all resource"
}

variable "isECR"{
  type = bool
  description = "want to configure image from ECR"
}

variable "service_name" {
  description = "App Runner service name"
}

variable "auto_scaling_configuration_name" {
  description = "Auto scaling configuration name"
}

variable "connection_arn" {
  description = "If isGithub true this variable is required"
}

//isECR = true
variable "image_repository_type" {
  description = "Type of ECR repository ECR | ECR_PUBLIC"
}

variable "image_identifier" {
  description = "ECR Image uri"
}

variable "auto_deployments_enabled" {
  type = bool
  description = "Auto Application deployment enable"
}

variable "app_runner_role" {
  description = "Iam role for ECR Image pull"
}

//isGithub = true
variable "build_command" {
  description = "Build command"
}

variable "runtime" {
  description = "application runtime environment"
}

variable "start_command" {
  description = "Application start command"
}

variable "configuration_source" {
  description = "configuration source REPOSITORY:reads configuration values from the apprunner.yaml in repository  | API:ignores the apprunner.yaml file"
}

variable "repository_url" {
  description = "Github repository URL"
}

variable "repository_branch" {
  description = "repository branch"
}

//Requiredt for both
variable "port" {
  description = "Image port"
}
