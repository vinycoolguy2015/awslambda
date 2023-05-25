locals {
  name = format(
    "%s-%s%s%s-%s",
    var.tags["Var1"],
    var.tags["Var2"],
    var.tags["Var3"],
    var.tags["var4"],
    var.name_suffix
  )
}

data "aws_caller_identity" "current" {}

resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
}

#Create S3 Bucket to receive incoming SES messages
resource "aws_s3_bucket" "ses_bucket" {
  bucket = "ses-bucket-${random_string.bucket_suffix.result}"
  tags = merge(
    var.tags
  )
}

resource "aws_s3_bucket_server_side_encryption_configuration" "ses" {
  bucket = aws_s3_bucket.ses_bucket.id
  rule {
    bucket_key_enabled = true
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_policy" "ses_bucket_policy" {
  bucket = aws_s3_bucket.ses_bucket.id
  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowSESPuts",
            "Effect": "Allow",
            "Principal": {
                "Service": "ses.amazonaws.com"
            },
            "Action": "s3:PutObject",
            "Resource": "${aws_s3_bucket.ses_bucket.arn}/*",
            "Condition": {
                "StringEquals": {
                    "aws:Referer": "${data.aws_caller_identity.current.account_id}"
                }
            }
        }
    ]
}
EOF
}

#Create IAM Role For Lambda functions
resource "aws_iam_role" "ses_lambda_role" {
  name               = format("iam-role-%s", local.name)
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
  tags = merge(
    var.tags,
    {
      Name = format("iam-role-%s", local.name)
    }
  )
}

resource "aws_iam_role_policy" "ses-lambda-role-policy" {
  name = format("iam-policy-%s", local.name)
  role = aws_iam_role.ses_lambda_role.id

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
            "Sid": "CloudWatchPermissions",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:CreateLogGroup",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        },
        {
            "Sid": "S3AndSESPermissions",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:DeleteObject",
                "s3:ListBucket",
                "ses:SendRawEmail",
                "ses:SendEmail"
            ],
            "Resource": [
                "${aws_s3_bucket.ses_bucket.arn}",
                "${aws_s3_bucket.ses_bucket.arn}/*",
                "arn:aws:ses:us-east-1:${data.aws_caller_identity.current.account_id}:identity/*",
                "arn:aws:ses:ap-southeast-1:${data.aws_caller_identity.current.account_id}:identity/*"
            ]
        }
    ]
    }
EOF


}

# Create Mail Forward Lambda functions

data "archive_file" "ses_email_forward_lambda" {
  type        = "zip"
  source_file = "${path.module}/ses_email_forward_lambda.py"
  output_path = "${path.module}/tmp/ses_email_forward_lambda.zip"
}

resource "aws_lambda_function" "ses_email_forward_lambda" {
  filename         = data.archive_file.ses_email_forward_lambda.output_path
  function_name    = format("lambda-%s", local.name)
  role             = aws_iam_role.ses_lambda_role.arn
  handler          = "ses_email_forward_lambda.lambda_handler"
  source_code_hash = data.archive_file.ses_email_forward_lambda.output_base64sha256
  timeout          = var.lambda_timeout
  memory_size      = var.lambda_memory_size
  runtime          = "python3.9"
  environment {
    variables = {
      ErrorNotificationRecipients = var.error_notification_recipients
      MailRecipient               = var.mail_recipient
      MailS3Bucket                = "${aws_s3_bucket.ses_bucket.id}"
      MailS3Prefix                = var.mail_s3_prefix
      MailSender                  = var.mail_sender
    }
  }
  tags = merge(
    var.tags,
    {
      Name = format("lambda-%s", local.name)
    }
  )
}

# Create Mail Forward Retry Lambda functions

data "archive_file" "ses_email_forward_retry_lambda" {
  type        = "zip"
  source_file = "${path.module}/ses_email_forward_retry_lambda.py"
  output_path = "${path.module}/tmp/ses_email_forward_retry_lambda.zip"
}

resource "aws_lambda_function" "ses_email_forward_retry_lambda" {
  filename         = data.archive_file.ses_email_forward_retry_lambda.output_path
  function_name    = format("lambda-%s-retry", local.name)
  role             = aws_iam_role.ses_lambda_role.arn
  handler          = "ses_email_forward_lambda.lambda_handler"
  source_code_hash = data.archive_file.ses_email_forward_retry_lambda.output_base64sha256
  timeout          = var.lambda_timeout
  memory_size      = var.lambda_memory_size
  runtime          = "python3.9"
  environment {
    variables = {
      ErrorNotificationRecipients = var.error_notification_recipients
      MailRecipient               = var.mail_recipient
      MailS3Bucket                = "${aws_s3_bucket.ses_bucket.id}"
      MailSender                  = var.mail_sender
    }
  }
  tags = merge(
    var.tags,
    {
      Name = format("lambda-%s-retry", local.name)
    }
  )
}


#Create SES Recipeint Rule Set 
resource "aws_ses_receipt_rule_set" "ses_receipt_rule_set" {
  rule_set_name = format("ses-rule-set-%s", local.name)

}

resource "aws_ses_receipt_rule" "ses_receipt_rule" {
  rule_set_name = aws_ses_receipt_rule_set.ses_receipt_rule_set.rule_set_name
  name          = format("ses-rule-%s", local.name)
  enabled       = true
  recipients    = [var.mail_sender]
  scan_enabled  = true
  tls_policy    = "Require"
  s3_action {
    bucket_name       = aws_s3_bucket.ses_bucket.id
    object_key_prefix = var.mail_s3_prefix
    position          = 1
  }

  lambda_action {
    function_arn    = aws_lambda_function.ses_email_forward_lambda.arn
    invocation_type = "Event"
    position        = 2

  }
  depends_on = [
    aws_lambda_permission.allow_ses_invoke
  ]
}

resource "aws_lambda_permission" "allow_ses_invoke" {
  statement_id  = "AllowExecutionFromSES"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ses_email_forward_lambda.function_name
  principal     = "ses.amazonaws.com"
  source_arn    = "arn:aws:ses:us-east-1:${data.aws_caller_identity.current.account_id}:receipt-rule-set/${aws_ses_receipt_rule_set.ses_receipt_rule_set.rule_set_name}:receipt-rule/${format("ses-rule-%s", local.name)}"
}

# Create CloudWatch Event Rule For SES Mail Forwarding Retry

resource "aws_cloudwatch_event_rule" "ses_mail_forward_retry" {
  name                = format("cw-event-%s", local.name)
  description         = "Trigger SES Mail Forward Retry Lambda"
  schedule_expression = "rate(1 hour)"
  is_enabled          = var.enable_cloudwatch_event_rule
  tags = merge(
    var.tags
  )
}

resource "aws_cloudwatch_event_target" "ses_mail_forward_retry" {
  rule      = aws_cloudwatch_event_rule.ses_mail_forward_retry.name
  target_id = format("cw-event-target-%s", local.name)
  arn       = aws_lambda_function.ses_email_forward_retry_lambda.arn
}

resource "aws_lambda_permission" "ses_mail_forward_retry" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ses_email_forward_retry_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.ses_mail_forward_retry.arn
}
