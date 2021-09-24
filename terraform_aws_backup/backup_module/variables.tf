variable "backup_vault_name" {
  type    = string
  default = "example-vault"
}

variable "retention" {
  type    = number
  default = 7
}

variable "schedule" {
  type    = string
  default = "cron(15 7 ? * MON-FRI *)"
}

variable "start_window" {
  type    = number
  default = 60
}

variable "completion_window" {
  type    = number
  default = 360
}

variable "name" {
  type    = string
  default = "example-backup"
}

variable "key" {
  type    = string
  default = "example"
}

variable "value" {
  type    = string
  default = "example"
}

variable "resources_arn" {
  type    = list(string)
  default = []
}

