module "networking" {
  source         = "./networking"
  vpc_name       = var.vpc_name
  vpc_cidr       = var.vpc_cidr
  public_subnet  = var.public_subnet
  private_subnet = var.private_subnet
}

module "iam" {
  source           = "./iam"
  ecs_cluster_name = var.ecs_cluster_name
}

module "ecs" {
  source                = "./ecs"
  depends_on            = [module.networking, module.loadbalancer]
  ecs_cluster_name      = var.ecs_cluster_name
  ecs_service_name      = var.ecs_service_name
  docker_image_url      = var.docker_image_url
  memory                = var.memory
  docker_container_port = var.docker_container_port
  desired_task_number   = var.desired_task_number
  message               = var.message
  private_subnets       = module.networking.private_subnets
  ecs_security_group    = module.security_group.ecs_security_group
  target_group_arn      = module.loadbalancer.ecs_target_group_arn
  execution_role_arn    = module.iam.execution_role_arn
  task_role_arn         = module.iam.task_role_arn
  cpu                   = var.cpu
}

module "security_group" {
  source                = "./security_group"
  vpc_id                = module.networking.vpc_id
  docker_container_port = var.docker_container_port
}

module "loadbalancer" {
  source                = "./loadbalancer"
  depends_on            = [module.networking]
  ecs_cluster_name      = var.ecs_cluster_name
  public_subnets_id     = module.networking.public_subnets
  alb_security_group_id = module.security_group.alb_security_group
  vpc_id                = module.networking.vpc_id
}

module "deployment" {
  source                           = "./deployment"
  depends_on                       = [module.loadbalancer, module.ecs]
  repo_name                        = var.repo_name
  ecs_cluster_name                 = var.ecs_cluster_name
  ecs_service_name                 = var.ecs_service_name
  env_name                         = var.env_name
  main_listener                    = module.loadbalancer.ecs_main_listener
  test_listener                    = module.loadbalancer.ecs_test_listener
  main_target_group                = module.loadbalancer.ecs_target_group
  test_target_group                = module.loadbalancer.ecs_test_target_group
  termination_wait_time_in_minutes = var.termination_wait_time_in_minutes
  deployment_config_name           = var.deployment_config_name
  ecr_repository_name              = var.ecr_repository_name
}
