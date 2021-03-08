variable "vpc_id" {
  type = string
}

variable "vpc_name" {
  type = string
}

variable "vpc_cidr" {
  type = string
}

variable "subnets" {
  type = map(any)
}

variable "subnet_count" {
  type = number
}