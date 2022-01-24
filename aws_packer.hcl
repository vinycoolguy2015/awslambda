packer {
  required_version = "1.7.9"
  required_plugins {
    amazon = {
      version = "1.0.0"
      source  = "github.com/hashicorp/amazon"
    }
  }
}


locals {
  ami_base_name                         = "aws-test"
  aws_region                            = "us-east-1"
  subnet_id                             = "subnet-07910a"
  temporary_security_group_source_cidrs = ["172.4.0.0/16"]
  associate_public_ip_address           = true
  ssh_interface                         = "private_ip"
  ebs_volume_size                       = "10"
  timestamp                             = formatdate("YYYYMMDDhhmm", timeadd(timestamp(), "8h"))
  ansible_vault_password_file           = "script.sh"
}

variable "environment" {
  type =   string
}

source "amazon-ebs" "aws-test {
  ami_name                              = "${local.ami_base_name}-${local.timestamp}"
  ami_description                       = "Standard Amazon Linux 2"
  instance_type                         = "t2.xlarge"
  region                                = "${local.aws_region}"
  subnet_id                             = "${local.subnet_id}"
  associate_public_ip_address           = "${local.associate_public_ip_address}"
  ssh_interface                         = "${local.ssh_interface}"
  temporary_security_group_source_cidrs = "${local.temporary_security_group_source_cidrs}"
  source_ami_filter {
    filters = {
      name                = "*Build_AML_2_*"
      architecture        = "x86_64"
      root-device-type    = "ebs"
      virtualization-type = "hvm"
    }
    most_recent = true
    owners      = ["272677"]
  }
  ami_block_device_mappings {
    device_name           = "/dev/xvda"
    volume_size           = "${local.ebs_volume_size}"
    volume_type           = "gp2"
    delete_on_termination = true
  }
  launch_block_device_mappings {
    device_name           = "/dev/xvda"
    volume_size           = "${local.ebs_volume_size}"
    volume_type           = "gp2"
    delete_on_termination = true
  }
  ssh_username = "ec2-user"
  tags = {
    Name      = "${local.ami_base_name}-${local.timestamp}"
    Base_Name = "${local.ami_base_name}"
    Timestamp = "${local.timestamp}"
    Packer    = "yes"
  }
  run_tags = {
    Name = "${local.ami_base_name}-${local.timestamp}-packer"
  }
}


build {
  name    = "aws-test-ami"
  sources = ["amazon-ebs.aws-test"]
  provisioner "ansible" {
    playbook_file   = "./playbook.yml"
    extra_arguments = ["-e", "environment=var.environment","--vault-password-file", "${local.ansible_vault_password_file}"]
  }
}
