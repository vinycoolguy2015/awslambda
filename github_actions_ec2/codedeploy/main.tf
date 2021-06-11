###################################Code Deploy 

resource "aws_codedeploy_app" "deployment" {
  compute_platform = "Server"
  name             = join("-", [var.env_name, "deployment"])
}

resource "aws_iam_role" "deployment" {
  name = join("-", [var.env_name, "deployment-role"])
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "codedeploy.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "AWSCodeDeployRole" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSCodeDeployRole"
  role       = aws_iam_role.deployment.name
}

resource "aws_codedeploy_deployment_group" "deployment" {
  app_name               = aws_codedeploy_app.deployment.name
  deployment_group_name  = join("-", [var.env_name, "deployment-group"])
  service_role_arn       = aws_iam_role.deployment.arn
  deployment_config_name = "CodeDeployDefault.OneAtATime" # AWS defined deployment config
  autoscaling_groups     = [join("_", [var.env_name, "webserver"])]
  deployment_style {
    deployment_option = "WITH_TRAFFIC_CONTROL"
    deployment_type   = "IN_PLACE"
  }
  load_balancer_info {
    target_group_info {
      name = join("-", [var.env_name, "target-group"])
    }
  }
  auto_rollback_configuration {
    enabled = true
    events = [
      "DEPLOYMENT_FAILURE",
    ]
  }
}
