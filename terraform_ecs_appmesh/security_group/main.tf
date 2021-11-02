resource "aws_security_group" "alb_sg" {
  name        = "ALB Security Group"
  description = "Application Load Balancer Security Group"
  vpc_id      = var.vpc_id
  ingress = [{
    from_port        = 80
    to_port          = 80
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    description      = "Allow HTTP Access On Port 80"
    ipv6_cidr_blocks = []
    prefix_list_ids  = []
    security_groups  = []
    self             = false
    }
  ]

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "ecs_sg" {
  name        = "ECS Security Group"
  description = "ECS Task Security Group"
  vpc_id      = var.vpc_id
  ingress = [
    {
      description      = "Allow access from ALB"
      from_port        = var.docker_container_port
      to_port          = var.docker_container_port
      protocol         = "tcp"
      security_groups  = [aws_security_group.alb_sg.id]
      ipv6_cidr_blocks = []
      prefix_list_ids  = []
      self             = false
      cidr_blocks      = []
    },
    {
      description      = "Allow access on Port 80"
      from_port        = 80
      to_port          = 80
      protocol         = "tcp"
      ipv6_cidr_blocks = []
      prefix_list_ids  = []
      self             = true
      security_groups  = []
      cidr_blocks      = []
    },
    {
      description      = "Allow access on Port 32000-33000"
      from_port        = 32000
      to_port          = 33000
      protocol         = "tcp"
      ipv6_cidr_blocks = []
      prefix_list_ids  = []
      self             = true
      security_groups  = []
      cidr_blocks      = []
    }
  ]

  egress = [
    {
      description      = "for all outgoing traffic"
      from_port        = 0
      to_port          = 0
      protocol         = "-1"
      cidr_blocks      = ["0.0.0.0/0"]
      ipv6_cidr_blocks = ["::/0"]
      prefix_list_ids  = []
      security_groups  = []
      self             = false
    }
  ]

}
