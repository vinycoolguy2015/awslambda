resource "aws_route53_resolver_firewall_domain_list" "allowed_domain" {
  name    = "allowed_domain"
  domains = ["*.amazonaws.com","google.com"]
}

resource "aws_route53_resolver_firewall_domain_list" "blocked_domain" {
  name    = "blocked_domain"
  domains = ["*"]
}

resource "aws_route53_resolver_firewall_rule_group" "dns_firewall" {
  name = "dns_firewall"
}

resource "aws_route53_resolver_firewall_rule" "allowed_domain" {
  name                    = "allowed_domain"
  action                  = "ALLOW"
  firewall_domain_list_id = aws_route53_resolver_firewall_domain_list.allowed_domain.id
  firewall_rule_group_id  = aws_route53_resolver_firewall_rule_group.dns_firewall.id
  priority                = 100
}

resource "aws_route53_resolver_firewall_rule" "blocked_domain" {
  name                    = "blocked_domain"
  action                  = "ALERT"
  firewall_domain_list_id = aws_route53_resolver_firewall_domain_list.blocked_domain.id
  firewall_rule_group_id  = aws_route53_resolver_firewall_rule_group.dns_firewall.id
  priority                = 200
}

resource "aws_route53_resolver_firewall_config" "dns_firewall" {
  resource_id        = var.vpc_id
  firewall_fail_open = "ENABLED"
}

resource "aws_route53_resolver_firewall_rule_group_association" "allowed_domain" {
  name                   = "dns_firewall"
  firewall_rule_group_id = aws_route53_resolver_firewall_rule_group.dns_firewall.id
  priority               = 101
  vpc_id                 = var.vpc_id
}

resource "aws_cloudwatch_log_group" "dns_firewall" {
  name = "/route53/dnsfirewall"
  retention_in_days = 30
}

resource "aws_route53_resolver_query_log_config" "dns_firewall" {
  name            = "dns_firewall"
  destination_arn = aws_cloudwatch_log_group.dns_firewall.arn
}

resource "aws_route53_resolver_query_log_config_association" "dns_firewall" {
  resolver_query_log_config_id = aws_route53_resolver_query_log_config.dns_firewall.id
  resource_id                  = var.vpc_id
}
