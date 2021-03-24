
#---------------------------------Key Pair
resource "aws_key_pair" "auth" {
  key_name   = "web_server"
  public_key = file(var.public_key_path)
}


#---------------------------------Create IAM Profile

resource "aws_iam_instance_profile" "webserver_profile" {
  name = "webserver_profile"
  role = aws_iam_role.role.name
  depends_on = [aws_iam_role.role]
}

resource "aws_iam_role" "role" {
  name = "webserver_role"
  path = "/"

  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "sts:AssumeRole",
            "Principal": {
               "Service": "ec2.amazonaws.com"
            },
            "Effect": "Allow",
            "Sid": ""
        }
    ]
}
EOF
}

resource "aws_iam_policy" "policy" {
  name        = "webserver-policy"
  description = "web server policy"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "rds:Describe*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "web-attach" {
  name       = "webserver-attachment"
  roles      = ["${aws_iam_role.role.name}"]
  policy_arn = aws_iam_policy.policy.arn
}

#---------------------------------Launch Configuration

resource "aws_launch_configuration" "web" {
  name_prefix   = "web-server-"
  image_id      = var.ami
  instance_type = var.instance_type
  key_name      = aws_key_pair.auth.id
  security_groups = [var.instance_sg]
  user_data = file(var.userdata)
  iam_instance_profile = aws_iam_instance_profile.webserver_profile.name
  lifecycle {
    create_before_destroy = true
  }
  depends_on = [aws_key_pair.auth]
}



#---------------------------------Auto Scaling Group

resource "aws_autoscaling_group" "web" {
  name                      = "web-server"
  max_size                  = 3
  min_size                  = 1
  health_check_grace_period = 300
  default_cooldown          = 300
  health_check_type         = "ELB"
  desired_capacity          = 1
  force_delete              = true
  launch_configuration      = aws_launch_configuration.web.name
  vpc_zone_identifier       = var.private_subnets
  depends_on = [aws_launch_configuration.web]
  tag {
    key                 = "Name"
    value               = "Web_Server"
    propagate_at_launch = true
  }
}

#---------------------------------ALB Target Group

resource "aws_lb_target_group" "web" {
  name     = "application-server-target-group"
  port     = 3000
  protocol = "HTTP"
  vpc_id   = var.vpcid
}


#---------------------------------ALB
resource "aws_lb" "web" {
  name               = "web-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [var.lb_sg]
  subnets            = var.public_subnets
  enable_cross_zone_load_balancing = true

  tags = {
    Name = "web-alb"
  }
}



#---------------------------------ALB Listener
resource "aws_lb_listener" "web_front_end" {
  load_balancer_arn = aws_lb.web.arn
  port              = "80"
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.web.arn
  }
}


#--------------------------------Target Group Attachment
resource "aws_autoscaling_attachment" "asg_attachment_web" {
  autoscaling_group_name = aws_autoscaling_group.web.id
  alb_target_group_arn   = aws_lb_target_group.web.arn
}


#--------------------------------Cloud Watch Alarm

resource "aws_cloudwatch_metric_alarm" "high" {
  alarm_name                = "cpu-high-utilization"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = "2"
  metric_name               = "CPUUtilization"
  namespace                 = "AWS/EC2"
  period                    = "60"
  statistic                 = "Average"
  threshold                 =  var.highcpu
  alarm_description         = "Scale down web servers when CPU utilization is more than threshold"
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.web.name
  }
  alarm_actions     = [aws_autoscaling_policy.scaleup.arn]
  depends_on = [aws_autoscaling_group.web]
}

resource "aws_cloudwatch_metric_alarm" "low" {
  alarm_name                = "cpu-low-utilization"
  comparison_operator       = "LessThanOrEqualToThreshold"
  evaluation_periods        = "2"
  metric_name               = "CPUUtilization"
  namespace                 = "AWS/EC2"
  period                    = "60"
  statistic                 = "Average"
  threshold                 =  var.lowcpu
  alarm_description         = "Scale down web servers when CPU utilization is less than threshold"
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.web.name
  }
  alarm_actions     = [aws_autoscaling_policy.scaledown.arn]
  depends_on = [aws_autoscaling_group.web]
}


#--------------------------------Auto Scaling Policies

resource "aws_autoscaling_policy" "scaleup" {
  name                   = "add-web-server-instance"
  scaling_adjustment     = 1
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 300
  autoscaling_group_name = aws_autoscaling_group.web.name
  depends_on = [aws_autoscaling_group.web]
}

resource "aws_autoscaling_policy" "scaledown" {
  name                   = "remove-web-server-instance"
  scaling_adjustment     = -1
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 300
  autoscaling_group_name = aws_autoscaling_group.web.name
  depends_on = [aws_autoscaling_group.web]
}
