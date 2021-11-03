resource "aws_iam_policy" "state_machine_iam_policy" {
  name        = "patching_state_machine_iam_policy"
  path        = "/"
  description = "patching_state_machine_iam_policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "lambda:InvokeFunction",
        ]
        Effect   = "Allow"
        Resource = values(aws_lambda_function.patching_workflow_lambda)[*].arn
      },
    ]
  })
}

resource "aws_iam_role" "iam_for_state_machine" {
  name               = "iam_role_for_patching_state_machine"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "states.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "state_machine_policy_attachment" {
  role       = aws_iam_role.iam_for_state_machine.name
  policy_arn = aws_iam_policy.state_machine_iam_policy.arn
}


resource "aws_iam_role" "iam_for_lambda" {
  name               = "iam_role_for_patching_lambda_functions"
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

resource "aws_iam_policy" "lambda_function_policy" {
  name        = "iam_policy_for_patching_lambda_functions"
  path        = "/"
  description = "iam_role_for_patching_lambda_functions"
  policy      = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*",
      "Effect": "Allow"
    },
{
            
            "Effect": "Allow",
            "Action": [
                "ssm:SendCommand",
                "ec2:DescribeImages",
                "ec2:DescribeInstances",
                "sns:Publish",
                "ssm:DescribeInstancePatchStates",
                "ec2:CreateImage",
                "ec2:CreateTags",
                "ssm:DescribeInstancePatches",
                "ssm:GetCommandInvocation"
            ],
            "Resource": "*"
        }
    
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  role       = aws_iam_role.iam_for_lambda.name
  policy_arn = aws_iam_policy.lambda_function_policy.arn
}


resource "aws_sns_topic" "patching_sns_topic" {
  name = "patching_sns_topic"
}

resource "aws_lambda_function" "patching_workflow_lambda" {
  for_each         = fileset(path.module, "code/*.zip")
  filename         = each.key
  function_name    = split(".", split("/", each.key)[1])[0]
  role             = aws_iam_role.iam_for_lambda.arn
  handler          = join(".", [split(".", split("/", each.key)[1])[0], "lambda_handler"])
  source_code_hash = filebase64sha256(each.key)
  runtime          = "python3.9"
  timeout          = 300
  dynamic "environment" {
   for_each = toset(each.key == "code/patching_completion_status.zip" ? ["set_sns_topic"] : [])
   content {
    variables = {
      SNS_TOPIC = aws_sns_topic.patching_sns_topic.arn
  }
   }
}
}



resource "aws_sfn_state_machine" "patching_state_machine" {
  name       = "patching_state_machine"
  role_arn   = aws_iam_role.iam_for_state_machine.arn
  definition = data.template_file.patching_state_machine_definition.rendered
}


data "template_file" "patching_state_machine_definition" {
  template = file("code/state_machine_definition.json")
  vars = {
    aws_account_id = var.aws_account_id
    aws_region     = var.aws_region
  }
}
