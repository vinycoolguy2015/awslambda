variable "subnet_count" {
}

variable "vpc_cidr" {
}

variable "vpc_private_subnet_cidrs" {
  type = list(string)
}

variable "vpc_public_subnet_cidrs" {
  type = list(string)
}

variable "db_storage" {
}


variable "dbinstance_class" {
}

variable "dbuser" {
}

variable "dbpassword" {
}

variable "rds_name" {
}

variable "aws_region" {
}


variable "highcpu" {
}

variable "lowcpu" {
}

variable "ami" {
}


variable "instance_type" {
}


variable "public_key_path" {
}

variable "userdata" {
}
