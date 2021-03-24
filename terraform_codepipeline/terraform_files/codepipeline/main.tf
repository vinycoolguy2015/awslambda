resource "aws_s3_bucket" "codepipeline_bucket" {
  bucket = join("-", [lower(var.env_name), "bucket1989"])
  acl    = "private"
}

resource "aws_iam_role" "codepipeline_role" {
  name = join("-", [var.env_name, "codepipeline"])

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "codepipeline.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "codepipeline_policy" {
  name = "codepipeline_policy"
  role = aws_iam_role.codepipeline_role.id

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect":"Allow",
      "Action": [
        "s3:GetObject",
        "s3:GetObjectVersion",
        "s3:GetBucketVersioning",
        "s3:PutObject"
      ],
      "Resource": [
        "${aws_s3_bucket.codepipeline_bucket.arn}",
        "${aws_s3_bucket.codepipeline_bucket.arn}/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "codebuild:BatchGetBuilds",
        "codebuild:StartBuild",
        "codedeploy:*"
      ],
      "Resource": "*"
    }
  ]
}
EOF
}




resource "aws_codepipeline" "web_pipeline" {
  name     = join("-", [var.env_name, "pipeline"])
  role_arn = aws_iam_role.codepipeline_role.arn
  tags = {
    Environment = var.env_name
  }

  artifact_store {
    location = aws_s3_bucket.codepipeline_bucket.bucket
    type     = "S3"
  }

  stage {
    name = "Source"
    action {
      category = "Source"
      configuration = {
        "OAuthToken"           = var.github_token
        "Branch"               = lower(var.env_name)
        "Owner"                = var.repository_owner
        "PollForSourceChanges" = "true"
        "Repo"                 = var.repository_name
      }
      input_artifacts = []
      name            = "Source"
      output_artifacts = [
        "SourceArtifact",
      ]
      owner     = "ThirdParty"
      provider  = "GitHub"
      run_order = 1
      version   = "1"
    }
  }

  stage {
    name = "Build"
    action {
      category = "Build"
      configuration = {
        "ProjectName" = join("-", [var.env_name, "build"])
      }
      input_artifacts = [
        "SourceArtifact",
      ]
      name = "Build"
      output_artifacts = [
        "BuildArtifact",
      ]
      owner     = "AWS"
      provider  = "CodeBuild"
      run_order = 1
      version   = "1"
    }
  }

  stage {
    name = "Deploy"
    action {
      name            = "Deploy"
      category        = "Deploy"
      owner           = "AWS"
      provider        = "CodeDeploy"
      input_artifacts = ["BuildArtifact"]
      run_order       = 1
      version         = "1"
      configuration = {
        ApplicationName     = aws_codedeploy_app.deployment.name
        DeploymentGroupName = aws_codedeploy_deployment_group.deployment.deployment_group_name
      }
    }
  }
}




##############################Code Build Project


resource "aws_iam_role" "codebuild" {
  name = join("-", [var.env_name, "codebuild"])

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "codebuild.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "codebuild" {
  role = aws_iam_role.codebuild.name

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Resource": [
        "*"
      ],
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "ec2:CreateNetworkInterface",
        "ec2:DescribeDhcpOptions",
        "ec2:DescribeNetworkInterfaces",
        "ec2:DeleteNetworkInterface",
        "ec2:DescribeSubnets",
        "ec2:DescribeSecurityGroups",
        "ec2:DescribeVpcs"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:*"
      ],
      "Resource": [
        "*"
      ]
    }
  ]
}
POLICY
}



resource "aws_codebuild_project" "web_build" {
  badge_enabled  = false
  build_timeout  = 60
  name           = join("-", [var.env_name, "build"])
  queued_timeout = 480
  service_role   = aws_iam_role.codebuild.arn

  artifacts {
    encryption_disabled    = false
    name                   = "web-build-${var.env_name}"
    override_artifact_name = false
    packaging              = "NONE"
    type                   = "CODEPIPELINE"
  }

  environment {
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = "aws/codebuild/amazonlinux2-x86_64-standard:2.0"
    image_pull_credentials_type = "CODEBUILD"
    privileged_mode             = false
    type                        = "LINUX_CONTAINER"
  }

  logs_config {
    cloudwatch_logs {
      status = "ENABLED"
    }

    s3_logs {
      encryption_disabled = false
      status              = "DISABLED"
    }
  }

  source {
    #buildspec           = data.template_file.buildspec.rendered
    git_clone_depth     = 0
    insecure_ssl        = false
    report_build_status = false
    type                = "CODEPIPELINE"
  }
}

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
    deployment_type   = "BLUE_GREEN"
  }
  load_balancer_info {
    target_group_info {
      name = join("-", [var.env_name, "target-group"])
    }
  }
  blue_green_deployment_config {
    deployment_ready_option {
      action_on_timeout = "CONTINUE_DEPLOYMENT"
    }
    green_fleet_provisioning_option {
      action = "COPY_AUTO_SCALING_GROUP"
    }
    terminate_blue_instances_on_deployment_success {
      action = "KEEP_ALIVE"
    }
  }
  auto_rollback_configuration {
    enabled = true
    events = [
      "DEPLOYMENT_FAILURE",
    ]
  }
}
