locals {
  chatbot_slack_workspace_id = "TA2E"
}

data "aws_caller_identity" "current" {}

resource "aws_cloudwatch_event_rule" "eks" {
  name        = "capture-eks-api-calls"
  description = "Capture EKS Config Change API calls"
  event_pattern = <<EOF
  {
  "source": ["aws.eks"],
  "detail-type": ["AWS API Call via CloudTrail"],
  "detail": {
    "eventSource": ["eks.amazonaws.com"],
    "eventName": ["CreateCluster", "DeleteCluster", "DeleteFargateProfile", "CreateFargateProfile", "UpdateClusterVersion"]
  }
}
  EOF
}

resource "aws_cloudwatch_event_target" "sns" {
  rule      = aws_cloudwatch_event_rule.eks.name
  target_id = "SendToSNS"
  arn       = aws_sns_topic.eks.arn
}


# SNS
resource "aws_sns_topic" "eks" {
  name = "eks"
}

resource "aws_sns_topic_policy" "eks" {
  arn    = aws_sns_topic.eks.arn
  policy = data.aws_iam_policy_document.eks.json
}

data "aws_iam_policy_document" "eks" {
  policy_id = "__default_policy_ID"
  statement {
    actions = [
      "SNS:Subscribe",
      "SNS:SetTopicAttributes",
      "SNS:RemovePermission",
      "SNS:Receive",
      "SNS:Publish",
      "SNS:ListSubscriptionsByTopic",
      "SNS:GetTopicAttributes",
      "SNS:DeleteTopic",
      "SNS:AddPermission"
    ]

    condition {
      test     = "StringEquals"
      variable = "AWS:SourceOwner"

      values = [
        data.aws_caller_identity.current.id,
      ]
    }

    effect = "Allow"

    principals {
      type        = "AWS"
      identifiers = ["*"]
    }

    resources = [
      aws_sns_topic.eks.arn,
    ]

    sid = "__default_statement_ID"
  }
  statement {
    actions = [
      "SNS:Publish"
    ]

    principals {
      type        = "Service"
      identifiers = ["events.amazonaws.com"]
    }
    resources = [
      aws_sns_topic.eks.arn,
    ]
  }
}


# Slack Bot

module "chatbot-slack-critical" {
  source             = "waveaccounting/chatbot-slack-configuration/aws"
  version            = "1.1.0"
  logging_level      = "NONE"
  configuration_name = "eks"
  iam_role_arn       = aws_iam_role.chatbot_iam_role.arn
  slack_channel_id   = "CA881" # general
  slack_workspace_id = local.chatbot_slack_workspace_id
  guardrail_policies = ["arn:aws:iam::aws:policy/ReadOnlyAccess"]
  sns_topic_arns     = [aws_sns_topic.eks.arn]

}

# Role

data "aws_iam_policy_document" "chatbot_iam_policy_document" {

  statement {
    effect    = "Allow"
    actions   = [ "cloudwatch:Describe*", "cloudwatch:Get*","cloudwatch:List*"]
    resources = ["*"]
  }

}

resource "aws_iam_policy" "chatbot_iam_policy" {
  name   = "chatbot-role-policy"
  policy = data.aws_iam_policy_document.chatbot_iam_policy_document.json
}

data "aws_iam_policy_document" "chatbot_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["chatbot.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "chatbot_iam_role" {
  name = format("iam-role-%s", "chatbot_iam_role")
  assume_role_policy = data.aws_iam_policy_document.chatbot_assume_role_policy.json
 
}

resource "aws_iam_policy_attachment" "chatbot_iam_role_policy" {
  name = format("policy-attachment-%s", "chatbot_iam_role")
  roles      = [aws_iam_role.chatbot_iam_role.name]
  policy_arn = aws_iam_policy.chatbot_iam_policy.arn
}

