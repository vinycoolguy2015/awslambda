data "template_file" "ec2userdata_script" {
  template = file("ec2userdata_script.tpl")
  vars = {
    ENVIRONMENT = "qa"
  }
}


resource "aws_instance" "project-iac" {
  ami = "ami-033dd343cabeb"
  instance_type = "t2.micro"
  subnet_id = "subnet-1e21"
  associate_public_ip_address = true
  key_name = "dev"
  user_data = data.template_file.ec2userdata_script.rendered
  vpc_security_group_ids = [
    "sg-0e30f07a59"
  ]
  root_block_device {
    delete_on_termination = true
    volume_size = 10
    volume_type = "gp2"
  }
  tags = {
    Name ="TF"
  }

}
