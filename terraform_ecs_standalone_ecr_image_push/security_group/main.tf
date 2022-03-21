resource "aws_security_group" "ecs_sg" {
  name        = "ECS Security Group"
  description = "ECS Task Security Group"
  vpc_id      = var.vpc_id
  ingress {
    from_port       = var.docker_container_port
    to_port         = var.docker_container_port
    protocol        = "tcp"
    cidr_blocks      = [var.vpc_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
