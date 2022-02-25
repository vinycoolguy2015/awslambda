
resource "aws_cloudwatch_log_group" "springbootapp_log_group" {
  name = "${var.ecs_service_name}-LogGroup"
}

resource "aws_ecs_cluster" "fargate-cluster" {
  name = var.ecs_cluster_name
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

data "template_file" "ecs_task_definition_template" {
  template = file("${path.module}/task_definition.json")
  vars = {
    task_definition_name  = "${var.ecs_service_name}-container"
    ecs_service_name      = var.ecs_service_name
    docker_image_url      = var.docker_image_url
    memory                = var.memory
    docker_container_port = var.docker_container_port
    region                = var.region
    message               = var.message
  }
}

resource "aws_ecs_task_definition" "ecs-task-definition" {
  container_definitions    = data.template_file.ecs_task_definition_template.rendered
  family                   = var.ecs_service_name
  cpu                      = var.cpu
  memory                   = var.memory
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  execution_role_arn       = var.execution_role_arn
  task_role_arn            = var.task_role_arn
}


resource "aws_ecs_service" "ecs_service" {
  name            = var.ecs_service_name
  task_definition = aws_ecs_task_definition.ecs-task-definition.arn
  desired_count   = var.desired_task_number
  cluster         = aws_ecs_cluster.fargate-cluster.id
  launch_type     = "FARGATE"
  deployment_controller {
    type = "CODE_DEPLOY"
  }
  network_configuration {
    subnets          = var.private_subnets
    security_groups  = [var.ecs_security_group]
    assign_public_ip = false
  }

  load_balancer {
    container_name   = "${var.ecs_service_name}-container"
    container_port   = var.docker_container_port
    target_group_arn = var.target_group_arn
  }
  lifecycle {
    ignore_changes = [
      load_balancer,
      desired_count,
      task_definition
    ]
  }
}

