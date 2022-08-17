resource "aws_iam_role" "clamav_ecs_task_execution_iam_role" {
  name  = "iam-role-clamav-ecs-task-exe"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = ""
        Effect = "Allow"
        Action = "sts:AssumeRole"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
    }]
  })
}

resource "aws_iam_policy" "aws-ecs-task-exe-policy" {
  name  = "iam-policy-clamav-ecs-task-exe"
  path  = "/"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement : [
      {
        Effect = "Allow",
        Action = [
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
        ],
        Resource = "*"
      },
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "*"
      },
      {
        Sid      = "",
        Effect   = "Allow",
        Action   = ["ecr:GetAuthorizationToken"],
Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "aws-ecs-task-exe-policy" {
  policy_arn = aws_iam_policy.aws-ecs-task-exe-policy.arn
  role       = aws_iam_role.clamav_ecs_task_execution_iam_role.name
}
