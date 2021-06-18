resource "random_id" "random_id_prefix" {
  byte_length = 2
}

module "iam" {
  source = "./modules/iam"

  region           = var.region
  environment      = var.environment
  random_id_prefix = random_id.random_id_prefix.hex
}


 module "apprunner" {
  source = "./modules/apprunner"
  region           = var.region
  environment      = var.environment
  random_id_prefix = random_id.random_id_prefix.hex

  isECR = var.isECR

  service_name                    = var.service_name
  auto_scaling_configuration_name = var.auto_scaling_configuration_name
  connection_arn                  = var.connection_arn

  //isECR = true
  image_repository_type    = var.image_repository_type
  image_identifier         = var.image_identifier
  auto_deployments_enabled = var.auto_deployments_enabled
  app_runner_role          = module.iam.app_runner_role

  //isGithub = true
  build_command        = var.build_command
  runtime              = var.runtime
  start_command        = var.start_command
  configuration_source = var.configuration_source
  repository_url       = var.repository_url
  repository_branch    = var.repository_branch

  //Requiredt for both
  port = var.port
}
