resource "aws_wafv2_web_acl" "this" {
  name  = var.name
  scope = "CLOUDFRONT"

  default_action {
    block {}
  }
  dynamic "rule" {
    for_each = var.enable_geo == true ? [1] : []
    content {
      name     = "Geo"
      priority = 1
      action {
        block {}
      }
      statement {
        not_statement {
          statement {

            geo_match_statement {
              country_codes = ["SG"]
            }
          }
        }
      }


      visibility_config {
        cloudwatch_metrics_enabled = true
        metric_name                = "AWSDomesticDOS"
        sampled_requests_enabled   = true
      }





    }
  }


  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = "AWSDomesticDOS"
    sampled_requests_enabled   = true
  }

}
