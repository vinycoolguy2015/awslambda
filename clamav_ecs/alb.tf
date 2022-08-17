resource "aws_lb" "test_aws_alb" {
  name                       = "alb-clamav"
  internal                   = false
  load_balancer_type         = "application"
  security_groups            = [aws_security_group.lb-sg.id]
  subnets                    = var.application_subnets
  drop_invalid_header_fields = true
  enable_deletion_protection = true
}

resource "aws_lb_listener" "test_lb_listener_main" {
  load_balancer_arn = aws_lb.test_aws_alb.arn
  port              = "80"
  protocol = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.test_target_group.arn
  }
}


resource "aws_lb_target_group" "test_target_group" {
  name        = "lbtg-clamav"
  port        = 8080
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"
  health_check {
    path              = var.healthcheck_path
    healthy_threshold = 5
    matcher           = "200,301,401-499"
  }
}
