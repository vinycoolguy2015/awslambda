variable "subnet_ids" {
  type        = list(string)
  description = "(Required) List of Subnets to use for Cluster Group"
}
variable "table_arn" {
  type        = string
  description = "(Required) DynamoDB Table ARN"
}

variable "vpc_cidr" {
  type        = string
  description = "(Required) VPC CIDR Range"
}
