output "execution_role_arn" {
  value = aws_iam_role.ecs_cluster_ecstaskrole.arn
}

output "task_role_arn" {
  value = aws_iam_role.ecs_cluster_ecstaskrole.arn
}
