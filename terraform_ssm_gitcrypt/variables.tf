variable "ssm_kms_key_id" {
  description = "SSM KMS Key ID."
  type        = string
}

variable "ssm_secure" {
  description = "Map of SSM parameters to be stored in securestring"
  type        = any
  default     = {}
}
