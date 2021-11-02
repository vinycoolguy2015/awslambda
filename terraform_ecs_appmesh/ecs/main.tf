
resource "aws_cloudwatch_log_group" "ecs_log_group" {
  name = "/ecs/microservice-demo"
}

resource "aws_ecs_cluster" "fargate-cluster" {
  name = var.ecs_cluster_name
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_ecs_task_definition" "metal_ecs-task-definition" {
  container_definitions    = file("${path.module}/metal_task_definition.json")
  family                   = "metal"
  cpu                      = 512
  memory                   = 1024
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  execution_role_arn       = var.execution_role_arn
  task_role_arn            = var.task_role_arn
  proxy_configuration {
    type           = "APPMESH"
    container_name = "envoy"
    properties = {
      AppPorts         = "80"
      EgressIgnoredIPs = "169.254.170.2,169.254.169.254"
      IgnoredUID       = "1337"
      ProxyEgressPort  = 15001
      ProxyIngressPort = 15000
    }
  }
}

resource "aws_ecs_service" "metal_service" {
  name            = "metal"
  task_definition = aws_ecs_task_definition.metal_ecs-task-definition.arn
  desired_count   = 1
  cluster         = aws_ecs_cluster.fargate-cluster.id
  launch_type     = "FARGATE"
  service_registries {
    registry_arn = aws_service_discovery_service.metal.arn
  }
  network_configuration {
    subnets          = var.private_subnets
    security_groups  = [var.ecs_security_group]
    assign_public_ip = false
  }


  lifecycle {
    ignore_changes = [
      task_definition
    ]
  }
}

resource "aws_ecs_task_definition" "pop_ecs-task-definition" {
  container_definitions    = file("${path.module}/pop_task_definition.json")
  family                   = "pop"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 512
  memory                   = 1024
  network_mode             = "awsvpc"
  execution_role_arn       = var.execution_role_arn
  task_role_arn            = var.task_role_arn
  proxy_configuration {
    type           = "APPMESH"
    container_name = "envoy"
    properties = {
      AppPorts         = "80"
      EgressIgnoredIPs = "169.254.170.2,169.254.169.254"
      IgnoredUID       = "1337"
      ProxyEgressPort  = 15001
      ProxyIngressPort = 15000
    }
  }
}

resource "aws_ecs_service" "pop_service" {
  name            = "pop"
  task_definition = aws_ecs_task_definition.pop_ecs-task-definition.arn
  desired_count   = 1
  cluster         = aws_ecs_cluster.fargate-cluster.id
  launch_type     = "FARGATE"
  service_registries {
    registry_arn = aws_service_discovery_service.pop.arn
  }
  network_configuration {
    subnets          = var.private_subnets
    security_groups  = [var.ecs_security_group]
    assign_public_ip = false
  }

  lifecycle {
    ignore_changes = [
      task_definition
    ]
  }
}

resource "aws_ecs_task_definition" "jukebox_ecs-task-definition" {
  container_definitions    = file("${path.module}/jukebox_task_definition.json")
  family                   = "jukebox"
  cpu                      = 512
  memory                   = 1024
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  execution_role_arn       = var.execution_role_arn
  task_role_arn            = var.task_role_arn
  proxy_configuration {
    type           = "APPMESH"
    container_name = "envoy"
    properties = {
      AppPorts         = "80"
      EgressIgnoredIPs = "169.254.170.2,169.254.169.254"
      IgnoredUID       = "1337"
      ProxyEgressPort  = 15001
      ProxyIngressPort = 15000
    }
  }
}

resource "aws_ecs_service" "jukebox_service" {
  name                              = "jukebox"
  task_definition                   = aws_ecs_task_definition.jukebox_ecs-task-definition.arn
  desired_count                     = 1
  cluster                           = aws_ecs_cluster.fargate-cluster.id
  launch_type                       = "FARGATE"
  health_check_grace_period_seconds = 60
  service_registries {
    registry_arn = aws_service_discovery_service.jukebox.arn
  }
  network_configuration {
    subnets          = var.private_subnets
    security_groups  = [var.ecs_security_group]
    assign_public_ip = false
  }

  load_balancer {
    container_name   = "jukebox"
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

resource "aws_service_discovery_private_dns_namespace" "ecs_namespace" {
  name        = "ecs-course.local"
  description = "ECS Service discovery namespace"
  vpc         = var.vpc_id
}

resource "aws_service_discovery_service" "metal" {
  name = "metal-service"

  dns_config {
    namespace_id = aws_service_discovery_private_dns_namespace.ecs_namespace.id

    dns_records {
      ttl  = 10
      type = "A"
    }

    routing_policy = "MULTIVALUE"
  }

  health_check_custom_config {
    failure_threshold = 1
  }
}

resource "aws_service_discovery_service" "pop" {
  name = "pop-service"

  dns_config {
    namespace_id = aws_service_discovery_private_dns_namespace.ecs_namespace.id

    dns_records {
      ttl  = 10
      type = "A"
    }

    routing_policy = "MULTIVALUE"
  }

  health_check_custom_config {
    failure_threshold = 1
  }
}

resource "aws_service_discovery_service" "jukebox" {
  name = "jukebox-service"

  dns_config {
    namespace_id = aws_service_discovery_private_dns_namespace.ecs_namespace.id

    dns_records {
      ttl  = 10
      type = "A"
    }

    routing_policy = "MULTIVALUE"
  }

  health_check_custom_config {
    failure_threshold = 1
  }
}
