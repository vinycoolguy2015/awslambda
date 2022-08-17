resource "aws_ecs_cluster" "fargate-cluster" {
  name = "clamav-cluster"
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_cloudwatch_log_group" "log_group" {
  name              = "clamav-logs"
}

resource "aws_ecs_task_definition" "internet_task_definition" {
  family = "ecs-clamav-task-defn"
  container_definitions = jsonencode([
    {
      name      = "clamav"
      image     = "clamav/clamav"
      essential = true

      healthCheck = {
        command     = ["CMD-SHELL", "netstat -nlp | grep -c 3310"]
        interval    = 10
        retries     = 3
        startPeriod = 60
        timeout     = 10
      }

      portMappings = [
        {
          containerPort = 3310
          hostPort      = 3310
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = "clamav-logs",
          awslogs-region        = var.aws_region,
          awslogs-stream-prefix = "clamav"
        }
      }
    },
    {
      name      = "clamav-api"
      image     = "registry.hub.docker.com/benzino77/clamav-rest-api:latest"
      essential = true

      portMappings = [
        {
          containerPort = 8080
          hostPort      = 8080
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = "clamav-logs",
          awslogs-region        = var.aws_region,
          awslogs-stream-prefix = "clamav"
        }
      }

      environment = [
        { "name" : "APP_FORM_KEY", "value" : "FILES" },
        { "name" : "APP_PORT", "value" : "8080" },
        { "name" : "CLAMD_IP", "value" : "localhost" },
        { "name" : "NODE_ENV", "value" : "production" }
      ]

      dependsOn = [{
        containerName = "clamav"
        condition     = "HEALTHY"
      }]
  }])
  requires_compatibilities = ["EC2", "FARGATE"]
  execution_role_arn       =  aws_iam_role.internet_ecs_task_execution_iam_role.arn
  cpu                      = 2048
  memory                   = 4096
  network_mode             = "awsvpc"
}

resource "aws_ecs_service" "internet_service" {
  name                              = "ecs-clamav-service"
  cluster                           = aws_ecs_cluster.fargate-cluster.id
  task_definition                   = aws_ecs_task_definition.internet_task_definition.arn
  desired_count                     = 1
  launch_type                       = "FARGATE"
  health_check_grace_period_seconds = 300
  load_balancer {
    target_group_arn = aws_lb_target_group.test_target_group.arn
    container_name   = "clamav-api"
    container_port   = 8080
  }
  network_configuration {
    subnets         = var.application_subnets
    security_groups = [aws_security_group.clamav-sg.id]
    assign_public_ip = true
  }
  enable_ecs_managed_tags = true
  propagate_tags          = "TASK_DEFINITION"
  deployment_controller {
    type = "ECS"
  }

  lifecycle {
    ignore_changes = [desired_count, task_definition, load_balancer]
  }
}

resource "aws_appautoscaling_target" "ecs_target" {
  max_capacity       =  3
  min_capacity       =  1
  resource_id        = "service/${aws_ecs_cluster.fargate-cluster.name}/${aws_ecs_service.internet_service.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}


resource "aws_appautoscaling_policy" "internet_memory_policy" {
  name               = "ecs-clamav-memory-autoscaling-policy"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.ecs_target.resource_id
  scalable_dimension = aws_appautoscaling_target.ecs_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.ecs_target.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageMemoryUtilization"
    }

    target_value = 80
  }
}

resource "aws_appautoscaling_policy" "internet_cpu_policy" {
  name               = "ecs-clamav-cpu-autoscaling-policy"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.ecs_target.resource_id
  scalable_dimension = aws_appautoscaling_target.ecs_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.ecs_target.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    target_value = 60
  }
}
