
#---------------------------------Key Pair
resource "aws_key_pair" "auth" {
  key_name   = join("_", [var.env_name, "webserver_key"])
  public_key = file(var.public_key_path)
}


#---------------------------------Create IAM Profile

resource "aws_iam_instance_profile" "webserver_profile" {
  name       = join("_", [var.env_name, "webserver_profile"])
  role       = aws_iam_role.role.name
  depends_on = [aws_iam_role.role]
}

resource "aws_iam_role" "role" {
  name = join("_", [var.env_name, "webserver_role"])
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
  name        = join("_", [var.env_name, "webserver_policy"])
  description = "web server policy"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "rds:Describe*",
        "s3:*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "web-attach" {
  name       = join("_", [var.env_name, "webserver_policy_attachment"])
  roles      = [aws_iam_role.role.name]
  policy_arn = aws_iam_policy.policy.arn
}

#---------------------------------Launch Configuration

resource "aws_launch_configuration" "web" {
  name_prefix     = join("_", [var.env_name, "webserver_"])
  image_id        = var.ami
  instance_type   = var.instance_type
  key_name        = aws_key_pair.auth.id
  security_groups = [aws_security_group.instance_sg.id]
  user_data = templatefile(var.userdata, {
    env_name = var.env_name
    rds_name = var.rds_name
  })
  iam_instance_profile = aws_iam_instance_profile.webserver_profile.name
  lifecycle {
    create_before_destroy = true
  }
  depends_on = [aws_key_pair.auth]
}



#---------------------------------Auto Scaling Group

resource "aws_autoscaling_group" "web" {
  name                      = join("_", [var.env_name, "webserver"])
  max_size                  = 3
  min_size                  = 1
  health_check_grace_period = 300
  default_cooldown          = 300
  health_check_type         = "ELB"
  desired_capacity          = 1
  force_delete              = true
  launch_configuration      = aws_launch_configuration.web.name
  vpc_zone_identifier       = var.private_subnets
  depends_on                = [aws_launch_configuration.web, aws_db_instance.application]
  tag {
    key                 = "Name"
    value               = join("_", [var.env_name, "Web_Server"])
    propagate_at_launch = true
  }
  lifecycle {
    ignore_changes = [target_group_arns]
  }

}


#---------------------------------ALB Target Group

resource "aws_lb_target_group" "web" {
  name     = join("-", [var.env_name, "target-group"])
  port     = 3000
  protocol = "HTTP"
  vpc_id   = var.vpcid
}


#---------------------------------ALB
resource "aws_lb" "web" {
  name                             = join("-", [var.env_name, "alb"])
  internal                         = false
  load_balancer_type               = "application"
  security_groups                  = [aws_security_group.alb_sg.id]
  subnets                          = var.public_subnets
  enable_cross_zone_load_balancing = true

  tags = {
    Name = join("_", [var.env_name, "web_alb"])
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
  alarm_name          = join("_", [var.env_name, "cpu-high-utilization"])
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "60"
  statistic           = "Average"
  threshold           = var.highcpu
  alarm_description   = "Scale down web servers when CPU utilization is more than threshold"
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.web.name
  }
  alarm_actions = [aws_autoscaling_policy.scaleup.arn]
  depends_on    = [aws_autoscaling_group.web]
}

resource "aws_cloudwatch_metric_alarm" "low" {
  alarm_name          = join("_", [var.env_name, "cpu-low-utilization"])
  comparison_operator = "LessThanOrEqualToThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "60"
  statistic           = "Average"
  threshold           = var.lowcpu
  alarm_description   = "Scale down web servers when CPU utilization is less than threshold"
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.web.name
  }
  alarm_actions = [aws_autoscaling_policy.scaledown.arn]
  depends_on    = [aws_autoscaling_group.web]
}


#--------------------------------Auto Scaling Policies

resource "aws_autoscaling_policy" "scaleup" {
  name                   = join("_", [var.env_name, "add-web-server"])
  scaling_adjustment     = 1
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 300
  autoscaling_group_name = aws_autoscaling_group.web.name
  depends_on             = [aws_autoscaling_group.web]
}

resource "aws_autoscaling_policy" "scaledown" {
  name                   = join("_", [var.env_name, "remove-web-server"])
  scaling_adjustment     = -1
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 300
  autoscaling_group_name = aws_autoscaling_group.web.name
  depends_on             = [aws_autoscaling_group.web]
}


#---------------------------RDS Instance
resource "aws_db_instance" "application" {
  allocated_storage      = var.db_storage
  storage_type           = "gp2"
  engine                 = "mysql"
  engine_version         = "5.7"
  instance_class         = var.dbinstance_class
  name                   = "test"
  identifier             = join("-", [lower(var.env_name), var.rds_name])
  username               = var.dbuser
  password               = var.dbpassword
  skip_final_snapshot    = true
  parameter_group_name   = "default.mysql5.7"
  db_subnet_group_name   = var.dbsubnet
  multi_az               = false
  storage_encrypted      = true
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  tags = {
    Name = join("-", [var.env_name, var.rds_name])
  }
}


#--------------------------------------------------------------------- Create Security Group

resource "aws_security_group" "instance_sg" {
  name        = join("-", [var.env_name, "instance_sg"])
  description = "Web Server Security Group"
  vpc_id      = var.vpc_id
  ingress {
    from_port       = 3000
    to_port         = 3000
    protocol        = "tcp"
    security_groups = [aws_security_group.alb_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  lifecycle {
    create_before_destroy = true
  }

}

resource "aws_security_group" "alb_sg" {
  name        = join("-", [var.env_name, "alb_sg"])
  description = "Application Load Balancer Security Group"
  vpc_id      = var.vpc_id
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  lifecycle {
    create_before_destroy = true
  }
}


resource "aws_security_group" "rds_sg" {
  name        = join("-", [var.env_name, "rds_sg"])
  description = "RDS Instance Security Group"
  vpc_id      = var.vpc_id
  ingress {
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [aws_security_group.instance_sg.id]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  lifecycle {
    create_before_destroy = true
  }
}
