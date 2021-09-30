output "alb_security_group" {
  value = aws_security_group.alb_sg.id
}

output "ecs_security_group" {
  value = aws_security_group.ecs_sg.id
}
