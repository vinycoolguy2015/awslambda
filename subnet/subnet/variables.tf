variable "subnet_count" {
  type = number
}

variable "vpc_id" {
  type = string
}

variable "vpc_name" {
  type = string
}

variable "subnet_name" {
  type = string
}

variable "vpc_cidr" {
  type = string
}

variable "newbits" {
  type = number
}

variable "netnum" {
  type = number
}



variable "routes" {
  type=list(map(string))
}

variable "nacl_rules" {
  type=map(map(string))
}