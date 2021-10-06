data "template_file" "userdata_script" {
  template = "${file("userdata_script.tpl")}"
}


resource "aws_instance" "appian_ec2_node1" {
  ami                  = "ami-0b0af3577fe5e3532"
  instance_type        = "m4.large"
  key_name             = "vault"
  user_data            = data.template_file.userdata_script.rendered
  network_interface {
    network_interface_id = aws_network_interface.appian_inf_ec2_primary_1.id
    device_index         = 0
  }
  network_interface {
    network_interface_id = aws_network_interface.appian_inf_ec2_mgmt_1.id
    device_index         = 1
  }
  root_block_device {
    encrypted   = "true"
    volume_type = "gp2"
    volume_size = "10"
  }
}

#-- create network interface for the EC2 instance in first AZ
resource "aws_network_interface" "appian_inf_ec2_primary_1" {
  subnet_id       = "subnet-1e21093f"
  private_ips     = ["172.31.80.17"]
}

resource "aws_network_interface" "appian_inf_ec2_mgmt_1" {
  subnet_id       = "subnet-1e21093f"
  private_ips     = ["172.31.80.18"]
}
