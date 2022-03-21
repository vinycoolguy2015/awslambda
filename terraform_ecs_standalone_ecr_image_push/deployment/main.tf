resource "aws_codecommit_repository" "ecs" {
  repository_name = "ecsRepository"
  description     = "This is the repository for buildspec file"
}

resource "aws_cloudwatch_event_rule" "image_push" {
  name          = "ecr_image_push"
  role_arn      = aws_iam_role.cwe_role.arn
  event_pattern = <<EOF
{
  "source": [
    "aws.ecr"
  ],
  "detail": {
    "action-type": [
      "PUSH"
    ],
    "image-tag": [
      "latest"
    ],
    "repository-name": [
      "${var.ecr_repository_name}"
    ],
    "result": [
      "SUCCESS"
    ]
  },
  "detail-type": [
    "ECR Image Action"
  ]
}
EOF
}

resource "aws_cloudwatch_event_target" "codepipeline" {
  rule      = aws_cloudwatch_event_rule.image_push.name
  target_id = "${var.ecr_repository_name}-Image-Push-Codepipeline"
  arn       = aws_codepipeline.ecs_pipeline.arn
  role_arn  = aws_iam_role.cwe_role.arn
}


resource "aws_iam_role" "cwe_role" {
  name               = "${var.ecr_repository_name}-cwe-role"
  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "",
            "Effect": "Allow",
            "Principal": {
                "Service": ["events.amazonaws.com"]
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
EOF
}

resource "aws_iam_policy" "cwe_policy" {
  name = "${var.ecr_repository_name}-cwe-policy"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
        "Effect": "Allow",
        "Action": [
            "codepipeline:StartPipelineExecution"
        ],
        "Resource": [
            "${aws_codepipeline.ecs_pipeline.arn}"
        ]
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "cws_policy_attachment" {
  name       = "${var.ecr_repository_name}-cwe-policy"
  roles      = [aws_iam_role.cwe_role.name]
  policy_arn = aws_iam_policy.cwe_policy.arn
}

resource "aws_s3_bucket" "codepipeline_bucket" {
  bucket = join("-", [lower(var.env_name), "ecsbucket1989"])
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
        "ecs:*",
        "ecr:*"
      ],
      "Resource": "*"
    },
   {
            "Action": [
                "codecommit:CancelUploadArchive",
                "codecommit:GetBranch",
                "codecommit:GetCommit",
                "codecommit:GetRepository",
                "codecommit:GetUploadArchiveStatus",
                "codecommit:UploadArchive"
            ],
            "Resource": "*",
            "Effect": "Allow"
        },
{
            "Action": [
                "iam:PassRole"
            ],
            "Resource": "*",
            "Effect": "Allow",
            "Condition": {
                "StringEqualsIfExists": {
                    "iam:PassedToService": [
                        "ecs-tasks.amazonaws.com"
                    ]
                }
            }
        }
  ]
}
EOF
}

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
        "s3:*",
        "ecr:*"
      ],
      "Resource": [
        "*"
      ]
    }
  ]
}
POLICY
}



resource "aws_codebuild_project" "ecs_build" {
  badge_enabled  = false
  build_timeout  = 60
  name           = join("-", [var.env_name, "build"])
  queued_timeout = 480
  service_role   = aws_iam_role.codebuild.arn
  artifacts {
    encryption_disabled    = false
    name                   = "ecs-build-${var.env_name}"
    override_artifact_name = true
    packaging              = "NONE"
    type                   = "CODEPIPELINE"
  }

  environment {
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = "aws/codebuild/amazonlinux2-x86_64-standard:2.0"
    image_pull_credentials_type = "CODEBUILD"
    privileged_mode             = true
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
    git_clone_depth     = 0
    insecure_ssl        = false
    report_build_status = false
    type                = "CODEPIPELINE"
  }
}


resource "aws_codepipeline" "ecs_pipeline" {
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
      name             = "FetchCode"
      category         = "Source"
      owner            = "AWS"
      provider         = "CodeCommit"
      version          = "1"
      run_order        = 1
      output_artifacts = ["SourceArtifact"]
      configuration = {
        RepositoryName       = "ecsRepository"
        BranchName           = "main"
        PollForSourceChanges = true
      }
    }

    action {
      name             = "ImagePush"
      category         = "Source"
      owner            = "AWS"
      provider         = "ECR"
      version          = "1"
      output_artifacts = ["Image"]
      configuration = {
        RepositoryName = var.ecr_repository_name
        ImageTag       = "latest"
      }
    }
  }
  stage {
    name = "Build"
    action {
      category = "Build"
      configuration = {
        ProjectName = join("-", [var.env_name, "build"])
        PrimarySource = "SourceArtifact"
      }
      input_artifacts = [
        "SourceArtifact",
        "Image"
      ]
      name = "Build"
      output_artifacts = [
        "BuildArtifact"
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
      name      = "Deploy"
      category  = "Deploy"
      owner     = "AWS"
      provider  = "ECS"
      version   = "1"
      run_order = 1
      input_artifacts = [
        "BuildArtifact"
      ]
      configuration = {
        ClusterName       = var.ecs_cluster_name
        ServiceName       = var.ecs_service_name
        FileName          = "imageDefinitions.json"
        DeploymentTimeout = 15
      }
    }
  }
}




