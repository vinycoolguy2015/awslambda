resource "aws_apprunner_auto_scaling_configuration_version" "ngnix-apprunner-autoscaling" {
  auto_scaling_configuration_name = "${var.auto_scaling_configuration_name}${var.random_id_prefix}"
  max_concurrency = 100
  max_size        = 5
  min_size        = 1

  tags = {
    Name = var.auto_scaling_configuration_name
  }
}

resource "aws_apprunner_service" "ngnix-apprunner-service-ecr" {
  count = (var.isECR && var.image_repository_type == "ECR") ? 1 : 0

  service_name = "${var.service_name}${var.random_id_prefix}"

  source_configuration {
    image_repository {
      image_configuration {
        port = var.port
      }
      image_identifier      = var.image_identifier
      image_repository_type = var.image_repository_type
    }
    authentication_configuration{
      access_role_arn = var.app_runner_role
    }
    auto_deployments_enabled = var.auto_deployments_enabled
  }

  auto_scaling_configuration_arn = aws_apprunner_auto_scaling_configuration_version.ngnix-apprunner-autoscaling.arn

  health_check_configuration {
          healthy_threshold   = 1
          interval            = 10
          path                = "/"
          protocol            = "TCP"
          timeout             = 5
          unhealthy_threshold = 5
        }

        # instance_configuration {
        #   cpu               = 2048
        #   instance_role_arn = "arn:aws:iam::609906240783:role/service-role/AppRunnerECRAccessRole"
        #   memory            = 2048
        # }

  tags = {
    Name = var.service_name
  }
}

resource "aws_apprunner_service" "ngnix-apprunner-service-ecr-public" {
  count = (var.isECR && var.image_repository_type == "ECR_PUBLIC") ? 1 : 0

  service_name = "${var.service_name}${var.random_id_prefix}"

  source_configuration {
    image_repository {
      image_configuration {
        port = var.port
      }
      image_identifier      = var.image_identifier
      image_repository_type = var.image_repository_type
    }
    auto_deployments_enabled = false
  }

  auto_scaling_configuration_arn = aws_apprunner_auto_scaling_configuration_version.ngnix-apprunner-autoscaling.arn

  health_check_configuration {
          healthy_threshold   = 1
          interval            = 10
          path                = "/"
          protocol            = "TCP"
          timeout             = 5
          unhealthy_threshold = 5
        }

        # instance_configuration {
        #   cpu               = 2048
        #   instance_role_arn = "arn:aws:iam::609906240783:role/service-role/AppRunnerECRAccessRole"
        #   memory            = 2048
        # }

  tags = {
    Name = var.service_name
  }
}

resource "aws_apprunner_service" "ngnix-apprunner-service-github" {
  count = var.isECR ? 0 : 1
  service_name = "${var.service_name}${var.random_id_prefix}"

  source_configuration {
    authentication_configuration {
      connection_arn = var.connection_arn
    }
    code_repository {
      code_configuration {
        code_configuration_values {
          build_command = var.build_command
          port          = var.port
          runtime       = var.runtime
          start_command = var.start_command
        }
        configuration_source = var.configuration_source
      }
      repository_url = var.repository_url
      source_code_version {
        type  = "BRANCH"
        value = var.repository_branch
      }
    }
    auto_deployments_enabled = var.auto_deployments_enabled
  }

  auto_scaling_configuration_arn = aws_apprunner_auto_scaling_configuration_version.ngnix-apprunner-autoscaling.arn

  health_check_configuration {
          healthy_threshold   = 1
          interval            = 10
          path                = "/"
          protocol            = "TCP"
          timeout             = 5
          unhealthy_threshold = 5
        }

  tags = {
    Name = "${var.service_name}${var.random_id_prefix}"
  }
}

