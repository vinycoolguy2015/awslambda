output "ecs_target_group" {
  value = aws_alb_target_group.ecs_default_target_group.name
}

output "ecs_target_group_arn" {
  value = aws_alb_target_group.ecs_default_target_group.arn
}

output "ecs_test_target_group" {
  value = aws_alb_target_group.ecs_test_target_group.name
}

output "ecs_main_listener" {
  value = aws_alb_listener.ecs_alb_http_listener.arn
}

output "ecs_test_listener" {
  value = aws_alb_listener.ecs_alb_test_listener.arn
}

output "loadbalancer_dns" {
  value = aws_alb.ecs_cluster_alb.dns_name
}
