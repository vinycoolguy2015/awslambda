{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:CreateLogGroup",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:DeleteObject",
                "s3:ListBucket",
                "ses:SendRawEmail",
                "ses:SendEmail"
            ],
            "Resource": [
                "arn:aws:s3:::email-forwarding",
                "arn:aws:s3:::email-forwarding/*",
                "arn:aws:ses:us-east-1:<ACCOUNT_ID>:identity/*",
                "arn:aws:ses:ap-southeast-1:<ACCOUNT_ID>:identity/*"
            ]
        }
    ]
}
