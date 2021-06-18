/* role for Amazon CodePipeline */
resource "aws_iam_role" "app_runner_role" {
  name               = "${var.random_id_prefix}-apprunner-role"
  assume_role_policy = file("${path.module}/policies/app-runner-role.json")
}

resource "aws_iam_role_policy_attachment" "app_runner_attach" {
  role   = aws_iam_role.app_runner_role.id
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess"
}

resource "aws_iam_role_policy_attachment" "app_runner_attach_pipeline" {
  role   = aws_iam_role.app_runner_role.id
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}