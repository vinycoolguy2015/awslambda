locals {
  name = format(
    "%s-%s%s%s",
    var.tags["BU"],
    var.tags["Project"],
    var.tags["Env"],
    var.tags["Tier"]
  )

  all_tags = merge(
    var.tags,
    var.custom_tags
  )
}


#https://docs.aws.amazon.com/securityhub/latest/userguide/cloudwatch-controls.html
#[CloudWatch.1] A log metric filter and alarm should exist for usage of the root user

resource "aws_cloudwatch_log_metric_filter" "root_user_usage" {
  name           = format("cw-filter-%s-%s", local.name, "root_user_usage")
  log_group_name = var.log_group_name
  pattern        = "{$.userIdentity.type=\"Root\" && $.userIdentity.invokedBy NOT EXISTS && $.eventType !=\"AwsServiceEvent\"}"
  metric_transformation {
    name      = "root_user_usage"
    namespace = "securityhub_cloudwatch_controls"
    value     = "1"
    default_value = "0"
  }
}

resource "aws_cloudwatch_metric_alarm" "root_user_usage" {
  alarm_name          = format("cw-alarm-%s-%s", local.name, "root_user_usage")
  metric_name         = "root_user_usage"
  threshold           = "0"
  statistic           = "Sum"
  comparison_operator = "GreaterThanThreshold"
  datapoints_to_alarm = "1"
  evaluation_periods  = "1"
  period              = "60"
  namespace           = "securityhub_cloudwatch_controls"
  alarm_actions       = [var.sns_topic_arn]
  tags                = local.all_tags

}


#[CloudWatch.2] Ensure a log metric filter and alarm exist for unauthorized API calls

resource "aws_cloudwatch_log_metric_filter" "unauthorized_api_calls" {
  name           = format("cw-filter-%s-%s", local.name, "unauthorized_api_calls")
  log_group_name = var.log_group_name
  pattern        = "{($.errorCode=\"*UnauthorizedOperation\") || ($.errorCode=\"AccessDenied*\")}"
  metric_transformation {
    name      = "unauthorized_api_calls"
    namespace = "securityhub_cloudwatch_controls"
    value     = "1"
    default_value = "0"
  }
}

resource "aws_cloudwatch_metric_alarm" "unauthorized_api_calls" {
  alarm_name          = format("cw-alarm-%s-%s", local.name, "unauthorized_api_calls")
  metric_name         = "unauthorized_api_calls"
  threshold           = "0"
  statistic           = "Sum"
  comparison_operator = "GreaterThanThreshold"
  datapoints_to_alarm = "1"
  evaluation_periods  = "1"
  period              = "60"
  namespace           = "securityhub_cloudwatch_controls"
  alarm_actions       = [var.sns_topic_arn]
  tags                = local.all_tags
}

#[CloudWatch.3] Ensure a log metric filter and alarm exist for Management Console sign-in without MFA

resource "aws_cloudwatch_log_metric_filter" "management_console_sign_in_without_mfa" {
  name           = format("cw-filter-%s-%s", local.name, "management_console_sign_in_without_mfa")
  log_group_name = var.log_group_name
  pattern        = "{ ($.eventName = \"ConsoleLogin\") && ($.additionalEventData.MFAUsed != \"Yes\") && ($.userIdentity.type = \"IAMUser\") && ($.responseElements.ConsoleLogin = \"Success\") }"
  metric_transformation {
    name      = "management_console_sign_in_without_mfa"
    namespace = "securityhub_cloudwatch_controls"
    value     = "1"
    default_value = "0"
  }
}

resource "aws_cloudwatch_metric_alarm" "management_console_sign_in_without_mfa" {
  alarm_name          = format("cw-alarm-%s-%s", local.name, "management_console_sign_in_without_mfa")
  metric_name         = "management_console_sign_in_without_mfa"
  threshold           = "0"
  statistic           = "Sum"
  comparison_operator = "GreaterThanThreshold"
  datapoints_to_alarm = "1"
  evaluation_periods  = "1"
  period              = "60"
  namespace           = "securityhub_cloudwatch_controls"
  alarm_actions       = [var.sns_topic_arn]
  tags                = local.all_tags
}

#[CloudWatch.4] Ensure a log metric filter and alarm exist for IAM policy changes

resource "aws_cloudwatch_log_metric_filter" "iam_policy_change" {
  name           = format("cw-filter-%s-%s", local.name, "iam_policy_change")
  log_group_name = var.log_group_name
  pattern        = "{($.eventSource=iam.amazonaws.com) && (($.eventName=DeleteGroupPolicy) || ($.eventName=DeleteRolePolicy) || ($.eventName=DeleteUserPolicy) || ($.eventName=PutGroupPolicy) || ($.eventName=PutRolePolicy) || ($.eventName=PutUserPolicy) || ($.eventName=CreatePolicy) || ($.eventName=DeletePolicy) || ($.eventName=CreatePolicyVersion) || ($.eventName=DeletePolicyVersion) || ($.eventName=AttachRolePolicy) || ($.eventName=DetachRolePolicy) || ($.eventName=AttachUserPolicy) || ($.eventName=DetachUserPolicy) || ($.eventName=AttachGroupPolicy) || ($.eventName=DetachGroupPolicy))}"
  metric_transformation {
    name      = "iam_policy_change"
    namespace = "securityhub_cloudwatch_controls"
    value     = "1"
    default_value = "0"
  }
}

resource "aws_cloudwatch_metric_alarm" "iam_policy_change" {
  alarm_name          = format("cw-alarm-%s-%s", local.name, "iam_policy_change")
  metric_name         = "iam_policy_change"
  threshold           = "0"
  statistic           = "Sum"
  comparison_operator = "GreaterThanThreshold"
  datapoints_to_alarm = "1"
  evaluation_periods  = "1"
  period              = "60"
  namespace           = "securityhub_cloudwatch_controls"
  alarm_actions       = [var.sns_topic_arn]
  tags                = local.all_tags
}

#[CloudWatch.5] Ensure a log metric filter and alarm exist for CloudTrail AWS Configuration changes

resource "aws_cloudwatch_log_metric_filter" "cloudtrail_aws_configuration_change" {
  name           = format("cw-filter-%s-%s", local.name, "cloudtrail_aws_configuration_change")
  log_group_name = var.log_group_name
  pattern        = "{($.eventName=CreateTrail) || ($.eventName=UpdateTrail) || ($.eventName=DeleteTrail) || ($.eventName=StartLogging) || ($.eventName=StopLogging)}"
  metric_transformation {
    name      = "cloudtrail_aws_configuration_change"
    namespace = "securityhub_cloudwatch_controls"
    value     = "1"
    default_value = "0"
  }
}

resource "aws_cloudwatch_metric_alarm" "cloudtrail_aws_configuration_change" {
  alarm_name          = format("cw-alarm-%s-%s", local.name, "cloudtrail_aws_configuration_change")
  metric_name         = "cloudtrail_aws_configuration_change"
  threshold           = "0"
  statistic           = "Sum"
  comparison_operator = "GreaterThanThreshold"
  datapoints_to_alarm = "1"
  evaluation_periods  = "1"
  period              = "60"
  namespace           = "securityhub_cloudwatch_controls"
  alarm_actions       = [var.sns_topic_arn]
  tags                = local.all_tags
}

#[CloudWatch.6] Ensure a log metric filter and alarm exist for AWS Management Console authentication failures

resource "aws_cloudwatch_log_metric_filter" "aws_management_console_authentication_failures" {
  name           = format("cw-filter-%s-%s", local.name, "aws_management_console_authentication_failures")
  log_group_name = var.log_group_name
  pattern        = "{($.eventName=ConsoleLogin) && ($.errorMessage=\"Failed authentication\")}"
  metric_transformation {
    name      = "aws_management_console_authentication_failures"
    namespace = "securityhub_cloudwatch_controls"
    value     = "1"
    default_value = "0"
  }
}

resource "aws_cloudwatch_metric_alarm" "aws_management_console_authentication_failures" {
  alarm_name          = format("cw-alarm-%s-%s", local.name, "aws_management_console_authentication_failures")
  metric_name         = "aws_management_console_authentication_failures"
  threshold           = "0"
  statistic           = "Sum"
  comparison_operator = "GreaterThanThreshold"
  datapoints_to_alarm = "1"
  evaluation_periods  = "1"
  period              = "60"
  namespace           = "securityhub_cloudwatch_controls"
  alarm_actions       = [var.sns_topic_arn]
  tags                = local.all_tags
}

#[CloudWatch.7] Ensure a log metric filter and alarm exist for disabling or scheduled deletion of customer managed keys

resource "aws_cloudwatch_log_metric_filter" "disabling_or_scheduled_deletion_of_cmk" {
  name           = format("cw-filter-%s-%s", local.name, "disabling_or_scheduled_deletion_of_cmk")
  log_group_name = var.log_group_name
  pattern        = "{($.eventSource=kms.amazonaws.com) && (($.eventName=DisableKey) || ($.eventName=ScheduleKeyDeletion))}"
  metric_transformation {
    name      = "disabling_or_scheduled_deletion_of_cmk"
    namespace = "securityhub_cloudwatch_controls"
    value     = "1"
    default_value = "0"
  }
}

resource "aws_cloudwatch_metric_alarm" "disabling_or_scheduled_deletion_of_cmk" {
  alarm_name          = format("cw-alarm-%s-%s", local.name, "disabling_or_scheduled_deletion_of_cmk")
  metric_name         = "disabling_or_scheduled_deletion_of_cmk"
  threshold           = "0"
  statistic           = "Sum"
  comparison_operator = "GreaterThanThreshold"
  datapoints_to_alarm = "1"
  evaluation_periods  = "1"
  period              = "60"
  namespace           = "securityhub_cloudwatch_controls"
  alarm_actions       = [var.sns_topic_arn]
  tags                = local.all_tags
}

#[CloudWatch.8] Ensure a log metric filter and alarm exist for S3 bucket policy changes

resource "aws_cloudwatch_log_metric_filter" "s3_bucket_policy_changes" {
  name           = format("cw-filter-%s-%s", local.name, "s3_bucket_policy_changes")
  log_group_name = var.log_group_name
  pattern        = "{($.eventSource=s3.amazonaws.com) && (($.eventName=PutBucketAcl) || ($.eventName=PutBucketPolicy) || ($.eventName=PutBucketCors) || ($.eventName=PutBucketLifecycle) || ($.eventName=PutBucketReplication) || ($.eventName=DeleteBucketPolicy) || ($.eventName=DeleteBucketCors) || ($.eventName=DeleteBucketLifecycle) || ($.eventName=DeleteBucketReplication))}"
  metric_transformation {
    name      = "s3_bucket_policy_changes"
    namespace = "securityhub_cloudwatch_controls"
    value     = "1"
    default_value = "0"
  }
}

resource "aws_cloudwatch_metric_alarm" "s3_bucket_policy_changes" {
  alarm_name          = format("cw-alarm-%s-%s", local.name, "s3_bucket_policy_changes")
  metric_name         = "s3_bucket_policy_changes"
  threshold           = "0"
  statistic           = "Sum"
  comparison_operator = "GreaterThanThreshold"
  datapoints_to_alarm = "1"
  evaluation_periods  = "1"
  period              = "60"
  namespace           = "securityhub_cloudwatch_controls"
  alarm_actions       = [var.sns_topic_arn]
  tags                = local.all_tags
}

#[CloudWatch.9] Ensure a log metric filter and alarm exist for AWS Config configuration changes

resource "aws_cloudwatch_log_metric_filter" "aws_config_configuration_changes" {
  name           = format("cw-filter-%s-%s", local.name, "aws_config_configuration_changes")
  log_group_name = var.log_group_name
  pattern        = "{($.eventSource=config.amazonaws.com) && (($.eventName=StopConfigurationRecorder) || ($.eventName=DeleteDeliveryChannel) || ($.eventName=PutDeliveryChannel) || ($.eventName=PutConfigurationRecorder))}"
  metric_transformation {
    name      = "aws_config_configuration_changes"
    namespace = "securityhub_cloudwatch_controls"
    value     = "1"
    default_value = "0"
  }
}

resource "aws_cloudwatch_metric_alarm" "aws_config_configuration_changes" {
  alarm_name          = format("cw-alarm-%s-%s", local.name, "aws_config_configuration_changes")
  metric_name         = "aws_config_configuration_changes"
  threshold           = "0"
  statistic           = "Sum"
  comparison_operator = "GreaterThanThreshold"
  datapoints_to_alarm = "1"
  evaluation_periods  = "1"
  period              = "60"
  namespace           = "securityhub_cloudwatch_controls"
  alarm_actions       = [var.sns_topic_arn]
  tags                = local.all_tags
}

#[CloudWatch.10] Ensure a log metric filter and alarm exist for security group changes

resource "aws_cloudwatch_log_metric_filter" "security_group_changes" {
  name           = format("cw-filter-%s-%s", local.name, "security_group_changes")
  log_group_name = var.log_group_name
  pattern        = "{($.eventName=AuthorizeSecurityGroupIngress) || ($.eventName=AuthorizeSecurityGroupEgress) || ($.eventName=RevokeSecurityGroupIngress) || ($.eventName=RevokeSecurityGroupEgress) || ($.eventName=CreateSecurityGroup) || ($.eventName=DeleteSecurityGroup)}"
  metric_transformation {
    name      = "security_group_changes"
    namespace = "securityhub_cloudwatch_controls"
    value     = "1"
    default_value = "0"
  }
}

resource "aws_cloudwatch_metric_alarm" "security_group_changes" {
  alarm_name          = format("cw-alarm-%s-%s", local.name, "security_group_changes")
  metric_name         = "security_group_changes"
  threshold           = "0"
  statistic           = "Sum"
  comparison_operator = "GreaterThanThreshold"
  datapoints_to_alarm = "1"
  evaluation_periods  = "1"
  period              = "60"
  namespace           = "securityhub_cloudwatch_controls"
  alarm_actions       = [var.sns_topic_arn]
  tags                = local.all_tags
}

#[CloudWatch.11] Ensure a log metric filter and alarm exist for changes to Network Access Control Lists (NACL)

resource "aws_cloudwatch_log_metric_filter" "nacl_changes" {
  name           = format("cw-filter-%s-%s", local.name, "nacl_changes")
  log_group_name = var.log_group_name
  pattern        = "{($.eventName=CreateNetworkAcl) || ($.eventName=CreateNetworkAclEntry) || ($.eventName=DeleteNetworkAcl) || ($.eventName=DeleteNetworkAclEntry) || ($.eventName=ReplaceNetworkAclEntry) || ($.eventName=ReplaceNetworkAclAssociation)}"
  metric_transformation {
    name      = "nacl_changes"
    namespace = "securityhub_cloudwatch_controls"
    value     = "1"
    default_value = "0"
  }
}

resource "aws_cloudwatch_metric_alarm" "nacl_changes" {
  alarm_name          = format("cw-alarm-%s-%s", local.name, "nacl_changes")
  metric_name         = "nacl_changes"
  threshold           = "0"
  statistic           = "Sum"
  comparison_operator = "GreaterThanThreshold"
  datapoints_to_alarm = "1"
  evaluation_periods  = "1"
  period              = "60"
  namespace           = "securityhub_cloudwatch_controls"
  alarm_actions       = [var.sns_topic_arn]
  tags                = local.all_tags
}

#[CloudWatch.12] Ensure a log metric filter and alarm exist for changes to network gateway

resource "aws_cloudwatch_log_metric_filter" "network_gateway_changes" {
  name           = format("cw-filter-%s-%s", local.name, "network_gateway_changes")
  log_group_name = var.log_group_name
  pattern        = "{($.eventName=CreateCustomerGateway) || ($.eventName=DeleteCustomerGateway) || ($.eventName=AttachInternetGateway) || ($.eventName=CreateInternetGateway) || ($.eventName=DeleteInternetGateway) || ($.eventName=DetachInternetGateway)}"
  metric_transformation {
    name      = "network_gateway_changes"
    namespace = "securityhub_cloudwatch_controls"
    value     = "1"
    default_value = "0"
  }
}

resource "aws_cloudwatch_metric_alarm" "network_gateway_changes" {
  alarm_name          = format("cw-alarm-%s-%s", local.name, "network_gateway_changes")
  metric_name         = "network_gateway_changes"
  threshold           = "0"
  statistic           = "Sum"
  comparison_operator = "GreaterThanThreshold"
  datapoints_to_alarm = "1"
  evaluation_periods  = "1"
  period              = "60"
  namespace           = "securityhub_cloudwatch_controls"
  alarm_actions       = [var.sns_topic_arn]
  tags                = local.all_tags
}

#[CloudWatch.13] Ensure a log metric filter and alarm exist for route table changes

resource "aws_cloudwatch_log_metric_filter" "route_table_changes" {
  name           = format("cw-filter-%s-%s", local.name, "route_table_changes")
  log_group_name = var.log_group_name
  pattern        = "{($.eventSource=ec2.amazonaws.com) && (($.eventName=CreateRoute) || ($.eventName=CreateRouteTable) || ($.eventName=ReplaceRoute) || ($.eventName=ReplaceRouteTableAssociation) || ($.eventName=DeleteRouteTable) || ($.eventName=DeleteRoute) || ($.eventName=DisassociateRouteTable))}"
  metric_transformation {
    name      = "route_table_changes"
    namespace = "securityhub_cloudwatch_controls"
    value     = "1"
    default_value = "0"
  }
}

resource "aws_cloudwatch_metric_alarm" "route_table_changes" {
  alarm_name          = format("cw-alarm-%s-%s", local.name, "route_table_changes")
  metric_name         = "route_table_changes"
  threshold           = "0"
  statistic           = "Sum"
  comparison_operator = "GreaterThanThreshold"
  datapoints_to_alarm = "1"
  evaluation_periods  = "1"
  period              = "60"
  namespace           = "securityhub_cloudwatch_controls"
  alarm_actions       = [var.sns_topic_arn]
  tags                = local.all_tags
}

#[CloudWatch.14] Ensure a log metric filter and alarm exist for VPC changes

resource "aws_cloudwatch_log_metric_filter" "vpc_changes" {
  name           = format("cw-filter-%s-%s", local.name, "vpc_changes")
  log_group_name = var.log_group_name
  pattern        = "{($.eventName=CreateVpc) || ($.eventName=DeleteVpc) || ($.eventName=ModifyVpcAttribute) || ($.eventName=AcceptVpcPeeringConnection) || ($.eventName=CreateVpcPeeringConnection) || ($.eventName=DeleteVpcPeeringConnection) || ($.eventName=RejectVpcPeeringConnection) || ($.eventName=AttachClassicLinkVpc) || ($.eventName=DetachClassicLinkVpc) || ($.eventName=DisableVpcClassicLink) || ($.eventName=EnableVpcClassicLink)}"
  metric_transformation {
    name      = "vpc_changes"
    namespace = "securityhub_cloudwatch_controls"
    value     = "1"
    default_value = "0"
  }
}

resource "aws_cloudwatch_metric_alarm" "vpc_changes" {
  alarm_name          = format("cw-alarm-%s-%s", local.name, "vpc_changes")
  metric_name         = "vpc_changes"
  threshold           = "0"
  statistic           = "Sum"
  comparison_operator = "GreaterThanThreshold"
  datapoints_to_alarm = "1"
  evaluation_periods  = "1"
  period              = "60"
  namespace           = "securityhub_cloudwatch_controls"
  alarm_actions       = [var.sns_topic_arn]
  tags                = local.all_tags
}


