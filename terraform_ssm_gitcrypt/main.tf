data "aws_kms_key" "ssm" {
  key_id = var.ssm_kms_key_id
}

resource "aws_ssm_parameter" "secure" {
  for_each = local.ssm_secure

  name      = "/secure/${each.key}"
  value     = each.value
  type      = "SecureString"
  overwrite = true
  key_id    = data.aws_kms_key.ssm.id

}
