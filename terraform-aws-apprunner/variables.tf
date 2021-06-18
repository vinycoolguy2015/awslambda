variable "region" {
  description = "AWS Region"
  default     = "us-east-2"
}

variable "environment" {
  description = "The Deployment environment"
  default     = "dev"
}

variable "isECR" {
  type        = bool
  description = "want to configure image from ECR"
  default     = true
}

variable "service_name" {
  description = "App Runner service name"
  default     = "AppRunner_Service"
}

variable "auto_scaling_configuration_name" {
  description = "Auto scaling configuration name"
  default     = "Autoscaling_conf"
}

variable "connection_arn" {
  description = "If isGithub true this variable is required"
}

//isECR = true
variable "image_repository_type" {
  description = "Type of ECR repository ECR | ECR_PUBLIC"
  default     = "ECR_PUBLIC"
}

variable "image_identifier" {
  description = "ECR Image uri"
  default     = "public.ecr.aws/nginx/nginx:latest"
}

variable "auto_deployments_enabled" {
  type        = bool
  description = "Auto Application deployment enable"
  default     = false
}

//isGithub = true
variable "build_command" {
  description = "Build command"
  default     = "npm install"
}

variable "runtime" {
  description = "application runtime environment"
  default     = "NODEJS_12"
}

variable "start_command" {
  description = "Application start command"
  default     = "npm run start"
}

variable "configuration_source" {
  description = "configuration source REPOSITORY:reads configuration values from the apprunner.yaml in repository  | API:ignores the apprunner.yaml file"
  default     = "API"
}

variable "repository_url" {
  description = "Github repository URL"
  default     = "https://github.com/Prashant-jumpbyte/express-hello-world"
}

variable "repository_branch" {
  description = "repository branch"
  default     = "master"
}

//Requiredt for both
variable "port" {
  description = "Image port"
  default     = "3000"
}
