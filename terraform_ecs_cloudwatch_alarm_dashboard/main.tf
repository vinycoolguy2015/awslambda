data "archive_file" "ecs_cloudwatch" {
  type        = "zip"
  source_file = "${path.module}/ecs_cloudwatch.py"
  output_path = "${path.module}/tmp/ecs_cloudwatch.zip"
}

resource "aws_iam_role" "ecs_dashboard_role" {
  name = "iam-rle-${var.project_code}-ecs-dashboard-role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "ecs_dashboard_policy" {
  name = "iam-ply-${var.project_code}-ecs-dashboard-policy"
  role = aws_iam_role.ecs_dashboard_role.id

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "*",
      "Effect": "Allow"
    },
    {
        "Sid": "ObjectAcc",
        "Effect": "Allow",
        "Action": [
            "ecs:ListServices",
            "cloudwatch:PutDashboard",
            "cloudwatch:PutMetricAlarm", 
            "ecs:ListClusters"
        ],
        "Resource": "*"
    }
    
  ]
}
EOF
}

resource "aws_lambda_function" "ecs_dashboard" {
  filename         = data.archive_file.ecs_cloudwatch.output_path
  function_name    = "ecs_cloudwatch_lambda"
  role             = aws_iam_role.ecs_dashboard_role.arn
  handler          = "ecs_dashboard.lambda_handler"
  source_code_hash = data.archive_file.ecs_cloudwatch.output_base64sha256
  timeout          = 300
  runtime          = "python3.8"
  environment {
    variables = {
      sns_topic                  = var.sns_topic
      delayed_memory_utilized    = var.delayed_memory_utilized 
      delayed_cpu_utilized       = var.delayed_cpu_utilized
      delayed_task_count         = var.delayed_task_count
      passenger_memory_utilized  = var.passenger_memory_utilized
      passenger_cpu_utilized     = var.passenger_cpu_utilized
      passenger_task_count       = var.passenger_task_count
      apache_memory_utilized     = var.apache_memory_utilized
      apache_cpu_utilized        = var.apache_cpu_utilized
      apache_task_count          = var.apache_task_count
    }
  }

}
