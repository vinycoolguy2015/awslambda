resource "aws_iam_role" "ecs_cluster_autoscalingrole" {
  name               = "${var.ecs_cluster_name}-AutoscalingRole"
  assume_role_policy = <<EOF
{ 
"Version": "2012-10-17",
"Statement": [
 {
   "Effect": "Allow",
   "Principal": {
     "Service": ["application-autoscaling.amazonaws.com"]
   },
   "Action": "sts:AssumeRole"
  }
  ] 
 }
EOF
}

resource "aws_iam_role_policy" "ecs_cluster_autoscalingpolicy" {
  name   = "${var.ecs_cluster_name}-AutoscalingPolicy"
  role   = aws_iam_role.ecs_cluster_autoscalingrole.id
  policy = <<EOF
{ 
  "Version": "2012-10-17",
  "Statement": [    
    {
      "Effect": "Allow",
      "Action": [
        "application-autoscaling:*",
        "cloudwatch:DescribeAlarms", 
        "cloudwatch:PutMetricAlarm",
        "ecs:DescribeServices",
        "ecs:UpdateService"
      ],
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_role" "ecs_cluster_ecsrole" {
  name               = "${var.ecs_cluster_name}-ECSRole"
  assume_role_policy = <<EOF
{ 
"Version": "2012-10-17",
"Statement": [
 {
   "Effect": "Allow",
   "Principal": {
     "Service": ["ecs.amazonaws.com"]
   },
   "Action": "sts:AssumeRole"
  }
  ] 
 }
EOF
}

resource "aws_iam_role_policy" "ecs_cluster_policy" {
  name   = "${var.ecs_cluster_name}-ECSClusterPolicy"
  role   = aws_iam_role.ecs_cluster_ecsrole.id
  policy = <<EOF
{ 
  "Version": "2012-10-17",
  "Statement": [    
    {
      "Effect": "Allow",
      "Action": [
        "ec2:AttachNetworkInterface",
        "ec2:CreateNetworkInterface", 
        "ec2:CreateNetworkInterfacePermission",
        "ec2:DeleteNetworkInterface",
        "ec2:DeleteNetworkInterfacePermission",
        "ec2:Describe*",
        "ec2:DetachNetworkInterface",
        "elasticloadbalancing:DeregisterInstancesFromLoadBalancer",
        "elasticloadbalancing:DeregisterTargets",
        "elasticloadbalancing:Describe*",
        "elasticloadbalancing:RegisterInstancesWithLoadBalancer",
        "elasticloadbalancing:RegisterTargets"
      ],
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_role" "ecs_cluster_ecstaskrole" {
  name               = "${var.ecs_cluster_name}-ECSTaskRole"
  assume_role_policy = <<EOF
{ 
"Version": "2012-10-17",
"Statement": [
 {
   "Effect": "Allow",
   "Principal": {
     "Service": ["ecs-tasks.amazonaws.com"]
   },
   "Action": "sts:AssumeRole"
  }
  ] 
 }
EOF
}

resource "aws_iam_role_policy" "ecs_cluster_ecstaskpolicy" {
  name   = "${var.ecs_cluster_name}-ECSTaskPolicy"
  role   = aws_iam_role.ecs_cluster_ecstaskrole.id
  policy = <<EOF
{ 
  "Version": "2012-10-17",
  "Statement": [    
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
        ],
      "Resource": "*"
    }
  ]
}
EOF
}
