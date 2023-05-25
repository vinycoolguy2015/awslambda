variable "tags" {
  description = "A map of tags to add to all resources."
  type = object({
    Terraform    =  string
     Environment  = string
    
  })
}

variable "name_suffix" {
  description = "name suffix to be added in resource name"
  type        = string
  default     = "ses-forwarding"
}

variable "lambda_timeout" {
  description = "Lambda timout in seconds"
  type        = number
  default     = 900
}

variable "lambda_memory_size" {
  description = "Lambda Memory in MB"
  type        = number
  default     = 512
}

variable "mail_s3_prefix" {
  description = "folder name to be created in S3 bucket"
  type        = string
  default     = "incoming"
}

variable "mail_sender" {
  description = "email address used to forward mail"
  type        = string
}

variable "mail_recipient" {
  description = "email address to forward mail to"
  type        = string
}

variable "error_notification_recipients" {
  description = "email address to send mails when lambda encouners error while processing mails.You can specify multiple emails separated by a comma"
  type        = string
}

variable "enable_cloudwatch_event_rule" {
  description = "enable cloudwatch event rule to trigger ses rety lambda on  hourly basis "
  type        = bool
  default     = true
}

