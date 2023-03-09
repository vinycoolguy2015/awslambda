
#https://docs.aws.amazon.com/chatbot/latest/adminguide/getting-started.html#setting-up
#https://docs.aws.amazon.com/chatbot/latest/adminguide/slack-setup.html

locals {
  chatbot_slack_workspace_id = "TA2UL"
}

data "aws_caller_identity" "current" {}


# SNS
resource "aws_sns_topic" "critical" {
  name = "critical"
}

resource "aws_sns_topic_policy" "critical" {
  arn    = aws_sns_topic.critical.arn
  policy = data.aws_iam_policy_document.critical.json
}

data "aws_iam_policy_document" "critical" {
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
      aws_sns_topic.critical.arn,
    ]

    sid = "__default_statement_ID"
  }
  statement {
    actions = [
      "SNS:Publish"
    ]

    principals {
      type        = "Service"
      identifiers = ["cloudwatch.amazonaws.com"]
    }
    resources = [
      aws_sns_topic.critical.arn,
    ]
  }
}

resource "aws_sns_topic" "normal" {
  name = "normal"
}

resource "aws_sns_topic_policy" "normal" {
  arn    = aws_sns_topic.normal.arn
  policy = data.aws_iam_policy_document.normal.json
}

data "aws_iam_policy_document" "normal" {
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
      aws_sns_topic.normal.arn,
    ]

    sid = "__default_statement_ID"
  }
  statement {
    actions = [
      "SNS:Publish"
    ]

    principals {
      type        = "Service"
      identifiers = ["cloudwatch.amazonaws.com"]
    }
    resources = [
      aws_sns_topic.normal.arn,
    ]
  }
}



# Slack Bot

module "chatbot-slack-critical" {
  source             = "waveaccounting/chatbot-slack-configuration/aws"
  version            = "1.1.0"
  logging_level      = "NONE"
  configuration_name = "critical"
  iam_role_arn       = aws_iam_role.chatbot_iam_role.arn
  slack_channel_id   = "CA33" # general
  slack_workspace_id = local.chatbot_slack_workspace_id
  guardrail_policies = ["arn:aws:iam::aws:policy/ReadOnlyAccess"]
  sns_topic_arns     = [aws_sns_topic.critical.arn]

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

module "chatbot-slack-normal" {

  source             = "waveaccounting/chatbot-slack-configuration/aws"
  version            = "1.1.0"
  logging_level      = "NONE"
  configuration_name = "normal"
  iam_role_arn       = aws_iam_role.chatbot_iam_role.arn
  slack_channel_id   = "CA3PQ" # random
  slack_workspace_id = local.chatbot_slack_workspace_id
  guardrail_policies = ["arn:aws:iam::aws:policy/ReadOnlyAccess"]
  sns_topic_arns     = [aws_sns_topic.normal.arn]

}
 
# Now subscribe to one of these SNS topics for a CloudWatch Alarm 
# Trigger Alarm using aws cloudwatch set-alarm-state --alarm-name "Web_Server_CPU_Utilization" --state-value ALARM --state-reason "testing purposes"


aws cloudwatch set-alarm-state --alarm-name "Web_Server_CPU_Utilization" --state-value ALARM --state-reason "testing purposes"
