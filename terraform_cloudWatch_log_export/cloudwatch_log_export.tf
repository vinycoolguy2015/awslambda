data "archive_file" "log_exporter" {
  type        = "zip"
  source_file = "${path.module}/lambda/cloudwatch-to-s3.py"
  output_path = "${path.module}/lambda/tmp/cloudwatch-to-s3.zip"
}

data "aws_region" "current" {}

data "aws_caller_identity" "current" {}

resource "random_string" "random" {
  length  = 8
  special = false
  upper   = false
  number  = false
}

resource "aws_s3_bucket" "cloudwatch_log_bucket" {
  bucket = "cloudwatch-log-bucket-${random_string.random.result}"

}

resource "aws_s3_bucket_acl" "cloudwatch_log_bucket_acl" {
  bucket = aws_s3_bucket.cloudwatch_log_bucket.id
  acl    = "private"
}

resource "aws_s3_bucket_public_access_block" "cloudwatch_log_bucket_public_access_block" {
  bucket = aws_s3_bucket.cloudwatch_log_bucket.id
  block_public_acls   = true
  block_public_policy = true
  restrict_public_buckets = true
  ignore_public_acls =true
}

resource "aws_s3_bucket_policy" "cloudwatch_log_bucket_policy" {
  bucket = aws_s3_bucket.cloudwatch_log_bucket.id
  policy = <<POLICY
{    
    "Version": "2012-10-17",    
     "Statement": [
                {
                        "Effect": "Allow",
                        "Principal": {
                                "Service": "logs.us-east-1.amazonaws.com"
                        },
                        "Action": "s3:GetBucketAcl",
                        "Resource": "${aws_s3_bucket.cloudwatch_log_bucket.arn}"
                },
                {
                        "Effect": "Allow",
                        "Principal": {
                                "Service": "logs.us-east-1.amazonaws.com"
                        },
                        "Action": "s3:PutObject",
                        "Resource": "${aws_s3_bucket.cloudwatch_log_bucket.arn}/*",
                        "Condition": {
                                "StringEquals": {
                                        "s3:x-amz-acl": "bucket-owner-full-control"
                                }
                        }
                }
        ]
}
POLICY
}



resource "aws_iam_role" "log_exporter" {
  name = "log-exporter-${random_string.random.result}"

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

resource "aws_iam_role_policy" "log_exporter" {
  name = "log-exporter-${random_string.random.result}"
  role = aws_iam_role.log_exporter.id

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateExportTask",
        "logs:Describe*",
        "logs:ListTagsLogGroup"
      ],
      "Effect": "Allow",
      "Resource": "*"
    },
    {
      "Action": [
        "ssm:DescribeParameters",
        "ssm:GetParameter",
        "ssm:GetParameters",
        "ssm:GetParametersByPath",
        "ssm:PutParameter"
      ],
      "Resource": "arn:aws:ssm:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:parameter/log-exporter-last-export/*",
      "Effect": "Allow"
    },
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/log-exporter-*",
      "Effect": "Allow"
    },
    {
        "Sid": "ObjectAcc",
        "Effect": "Allow",
        "Action": [
            "s3:PutObject",
            "s3:PutObjectACL"
        ],
        "Resource": "${aws_s3_bucket.cloudwatch_log_bucket.arn}/*"
    },
    {
        "Sid": "AccountBucketAcc",
        "Effect": "Allow",
        "Action": [
            "s3:PutBucketAcl",
            "s3:GetBucketAcl"
        ],
        "Resource": "${aws_s3_bucket.cloudwatch_log_bucket.arn}"
    }
  ]
}
EOF
}

resource "aws_lambda_function" "log_exporter" {
  filename         = data.archive_file.log_exporter.output_path
  function_name    = "log-exporter-${random_string.random.result}"
  role             = aws_iam_role.log_exporter.arn
  handler          = "cloudwatch-to-s3.lambda_handler"
  source_code_hash = data.archive_file.log_exporter.output_base64sha256
  timeout          = 300

  runtime = "python3.8"

  environment {
    variables = {
      S3_BUCKET = aws_s3_bucket.cloudwatch_log_bucket.id
    }
  }
}

resource "aws_cloudwatch_event_rule" "log_exporter" {
  name                = "log-exporter-${random_string.random.result}"
  description         = "Fires periodically to export logs to S3"
  schedule_expression = "rate(4 hours)"
}

resource "aws_cloudwatch_event_target" "log_exporter" {
  rule      = aws_cloudwatch_event_rule.log_exporter.name
  target_id = "log-exporter-${random_string.random.result}"
  arn       = aws_lambda_function.log_exporter.arn
}

resource "aws_lambda_permission" "log_exporter" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.log_exporter.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.log_exporter.arn
}
