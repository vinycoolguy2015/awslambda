Note: For HCL templates, we need to make some changes. In your packer.hcl file, add 

variable "appian_environment" {
  type =   string
}

Change extra_arguments to 

"appian_environment=var.appian_environment"
