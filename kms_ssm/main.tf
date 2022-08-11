#Run encrypt.sh first to get the encrypted file

resource "aws_ssm_parameter" "main" {
  for_each = nonsensitive(yamldecode(data.aws_kms_secrets.secrets.plaintext.config))
  name     = each.key
  type     = "String"
  overwrite   = true
  value    = each.value
}

data "aws_kms_secrets" "secrets" {
  secret {
    name    = "config"
    payload = file("params.encrypted")
  }
}
