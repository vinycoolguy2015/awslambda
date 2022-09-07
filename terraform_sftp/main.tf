resource "aws_s3_bucket" "sftp-bucket" {
  bucket = var.bucket_name
}

resource "aws_s3_bucket_acl" "sftp-bucket-acl" {
  bucket = aws_s3_bucket.sftp-bucket.id
  acl    = "private"
}


resource "aws_iam_role" "logging" {
  name               = "${var.name}-transfer-logging"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "transfer.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "logging" {
  name   = "${var.name}-transfer-logging"
  role   = aws_iam_role.logging.id
  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogStream",
        "logs:DescribeLogStreams",
        "logs:CreateLogGroup",
        "logs:PutLogEvents"
      ],
      "Resource": "*"
    }
  ]
}
POLICY
}

resource "aws_transfer_server" "sftp" {
  endpoint_type          = "VPC"
  protocols              = ["SFTP"]
  identity_provider_type = "SERVICE_MANAGED"
  logging_role           = aws_iam_role.logging.arn
  force_destroy          = var.force_destroy
  security_policy_name   = var.security_policy_name
  endpoint_details {
    vpc_id             = var.vpc_id
    subnet_ids         = var.subnet_ids
    security_group_ids = [aws_security_group.sftp_vpc.id]
  }
}

resource "aws_security_group" "sftp_vpc" {
  name        = "${var.name}-sftp-vpc"
  description = "Security group for SFTP VPC"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
    description = "Allow connections from vpc cidr on port 22"
  }

  egress {
    from_port   = 1024
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
    description = "Allow outbound connections"
  }
}


resource "aws_iam_role" "user" {
  for_each           = var.sftp_users
  name               = "${var.name}-sftp-user-${each.key}"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "transfer.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "user" {
  for_each = var.sftp_users
  name     = "${var.name}-sftp-user-${each.key}"
  role     = aws_iam_role.user[each.key].id

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowListingOfUserFolder",
      "Action": [
        "s3:ListBucket",
        "s3:GetBucketLocation"
      ],
      "Effect": "Allow",
      "Resource": [
       "${join("", ["arn:aws:s3:::", var.bucket_name])}"
      ]
    },
    {
      "Sid": "HomeDirObjectAccess",
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObjectVersion",
        "s3:DeleteObject",
        "s3:GetObjectVersion"
      ],
      "Resource": "${join("", ["arn:aws:s3:::", var.bucket_name, "/", each.value, "/*"])}"
    }
  ]
}
POLICY
}

resource "aws_transfer_user" "this" {
  for_each       = var.sftp_users
  server_id      = aws_transfer_server.sftp.id
  user_name      = each.key
  home_directory = "/${var.bucket_name}/${each.value}"
  role           = aws_iam_role.user[each.key].arn
}

resource "aws_transfer_ssh_key" "this" {
  for_each   = var.sftp_users_ssh_key
  server_id  = aws_transfer_server.sftp.id
  user_name  = each.key
  body       = each.value
  depends_on = [aws_transfer_user.this]
}

resource "null_resource" "get-endpoint-dns" {
  provisioner "local-exec" {
    command = "aws ec2 describe-vpc-endpoints --vpc-endpoint-ids ${aws_transfer_server.sftp.endpoint_details[0].vpc_endpoint_id} --query 'VpcEndpoints[*].DnsEntries[0].DnsName'| jq .[0] |tr -d '\n'|tr -d '\"'> /tmp/dns.txt"
  }
}

data "local_file" "endpoint-dns" {
  filename   = "/tmp/dns.txt"
  depends_on = [null_resource.get-endpoint-dns]
}
