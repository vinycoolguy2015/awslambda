resource "aws_iam_role" "test_role" {
  count = var.env != "prod" && var.env != "stag" ? 1 : 0
  name = "test_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF

  tags = {
      tag-key = "tag-value"
  }
}

resource "aws_iam_instance_profile" "test_profile" {
  name = "test_profile"
  role = var.env != "prod" && var.env != "stag" ? aws_iam_role.test_role[0].name : var.role
}

resource "aws_iam_role_policy" "test_policy" {
  count = var.env != "prod" && var.env != "stag" ? 1 : 0
  name = "test_policy"
  role = aws_iam_role.test_role[0].name

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "s3:*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_instance" "role-test" {
  ami = "ami-0022f774911c1d690"
  subnet_id   ="subnet-82a486"
  instance_type = "t2.micro"
  iam_instance_profile = aws_iam_instance_profile.test_profile.name
  key_name = "test"
}
