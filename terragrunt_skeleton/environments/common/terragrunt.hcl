locals {
  vars                  = read_terragrunt_config(find_in_parent_folders("inputs.hcl"))
  environment           = local.vars.inputs["environment"]
  environment_state_key = local.environment != "lower" ? ".${local.environment}" : ""
  aws_region            = "ap-southeast-1"
  account_id            = "355"
}

remote_state {
  backend = "s3"
  config = {
    bucket         = "terraform"
    key            = "${path_relative_to_include()}${local.environment_state_key}"
    region         = "${local.aws_region}"
    encrypt        = true
    dynamodb_table = "lock-table"
  }
}

terraform {

  before_hook "copy_terraform_tf" {
    commands = ["init-from-module"]
    execute  = ["cp", "${get_parent_terragrunt_dir()}/terraform.tf", "."]
  }

  after_hook "rm_terraform_tf" {
    commands     = get_terraform_commands_that_need_vars()
    execute      = ["rm", "${get_terragrunt_dir()}/terraform.tf"]
    run_on_error = true
  }

  extra_arguments "common" {
    commands = get_terraform_commands_that_need_vars()
    required_var_files = [
      "${get_terragrunt_dir()}/${path_relative_from_include()}/common.tfvars"
    ]
  }
}

inputs = merge(
  local.vars.inputs,
  {
    key_name = "ec2-key"
    vpc_name = "vpc"
  }
)
