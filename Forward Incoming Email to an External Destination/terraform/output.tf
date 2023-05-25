output "ses_bucket" {
  value = aws_s3_bucket.ses_bucket.id
}
output "ses_forward_lambda_name" {
  value = aws_lambda_function.ses_email_forward_lambda.function_name
}

output "ses_forward_retry_lambda_name" {
  value = aws_lambda_function.ses_email_forward_lambda.function_name
}
