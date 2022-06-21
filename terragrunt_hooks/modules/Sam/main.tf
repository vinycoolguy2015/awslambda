resource "aws_ssm_parameter" "main" {
  for_each = var.params
  name     = "/api/cred/${each.key}"
  type     = "String"
  overwrite   = true
  value    = each.value
}
