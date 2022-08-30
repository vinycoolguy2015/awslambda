variable "bucket_name" {
  type        = string
  default     = "sftp2022"
  description = "Name of SFTP Bucket"
}

variable "vpc_cidr" {
  type        = string
  description = "VPC CIDR Of the VPC Used For Transfer Server"
}

variable "name" {
  type        = string
  default     = "test_server"
  description = "Name of SFTP server"
}

variable "vpc_id" {
  type        = string
  description = "VPC For Transfer Server"
}

variable "subnet_ids" {
  type        = list(string)
  description = "Subnets For Transfer Server"
}

variable "force_destroy" {
  type        = bool
  default     = true
  description = "Whether to delete all the users associated with server so that server can be deleted successfully."
}

variable "security_policy_name" {
  type        = string
  default     = "TransferSecurityPolicy-2020-06"
  description = "Specifies the name of the [security policy](https://docs.aws.amazon.com/transfer/latest/userguide/security-policies.html) to associate with the server"
}

variable "sftp_users" {
  type    = map(string)
  default = {}
}

variable "sftp_users_ssh_key" {
  type    = map(string)
  default = {}
}
