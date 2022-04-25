data "archive_file" "parameter_store" {
  type        = "zip"
  source_file = "${path.module}/lambda/parameter_store.py"
  output_path = "${path.module}/lambda/tmp/parameter_store.zip"
}

data "aws_region" "current" {}

data "aws_caller_identity" "current" {}

resource "random_string" "random" {
  length  = 8
  special = false
  upper   = false
  number  = false
}

resource "aws_iam_role" "parameter_store" {
  name = "parameter_store-${random_string.random.result}"

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

resource "aws_iam_role_policy" "parameter_store_policy" {
  name   = "parameter_store_policy-${random_string.random.result}"
  role   = aws_iam_role.parameter_store.id
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "ssm:DescribeParameters",
        "ssm:GetParameter"
      ],
      "Resource": "*",
      "Effect": "Allow"
    },
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/parameter_store-*",
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_lambda_function" "parameter_store_lambda" {
  filename         = data.archive_file.parameter_store.output_path
  function_name    = "parameter_store-${random_string.random.result}"
  role             = aws_iam_role.parameter_store.arn
  handler          = "parameter_store.lambda_handler"
  source_code_hash = data.archive_file.parameter_store.output_base64sha256
  timeout          = 300
  runtime          = "python3.9"
}

