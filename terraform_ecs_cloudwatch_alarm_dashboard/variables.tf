variable "sns_topic" {
  default     = "arn:aws:sns:ap-southeast-1:35571:SNS"
}

variable "delayed_memory_utilized" {
  type        = number
  default     = 1800
}

variable "delayed_cpu_utilized" {
  type        = number
  default     = 900
}

variable "delayed_task_count" {
  type        = number
  default     = 1
}

variable "passenger_memory_utilized" {
  type        = number
  default     = 1800
}

variable "passenger_cpu_utilized" {
  type        = number
  default     = 900
}

variable "passenger_task_count" {
  type        = number
  default     = 1
}

variable "apache_memory_utilized" {
  type        = number
  default     = 450
}

variable "apache_cpu_utilized" {
  type        = number
  default     = 200
}

variable "apache_task_count" {
  type        = number
  default     = 1
}
