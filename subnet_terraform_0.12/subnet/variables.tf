variable "vpc_id" {
  type = string
}

variable "vpc_name" {
  type = string
}

variable "subnet_count" {
  type = number
}

variable "subnets" {
  type = map(any)
}

variable "vpc_cidr" {
  type = string
}