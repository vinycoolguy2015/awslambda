data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["dax.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "role" {
  name               = "dax-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

data "aws_iam_policy_document" "policy" {
  statement {
    effect    = "Allow"
    actions   = ["dynamodb:DescribeTable","dynamodb:PutItem","dynamodb:GetItem","dynamodb:UpdateItem","dynamodb:DeleteItem","dynamodb:Query","dynamodb:Scan","dynamodb:BatchGetItem","dynamodb:BatchWriteItem","dynamodb:ConditionCheckItem"]
    resources = [var.table_arn]
  }
}

resource "aws_iam_policy" "policy" {
  name        = "dax-policy"
  description = "DAX policy"
  policy      = data.aws_iam_policy_document.policy.json
}

resource "aws_iam_role_policy_attachment" "dax-attach" {
  role       = aws_iam_role.role.name
  policy_arn = aws_iam_policy.policy.arn
}

# Create DAX Subnet Group
resource "aws_dax_subnet_group" "subnet_group" {
  name       = "dax-subnet"
  subnet_ids = var.subnet_ids
}

# Create DAX Security Group
resource "aws_security_group" "dax-sg" {
  name = "dax-sec-grp"
  description = "Allow Encrypted/Unecrypted traffic to DAX"

  ingress {
    from_port   = 8111
    to_port     = 8111
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  ingress {
    from_port   = 9111
    to_port     = 9111
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create DAX Cluster
resource "aws_dax_cluster" "cluster" {
  cluster_name       = "dax-cluster"
  iam_role_arn       = aws_iam_role.role.arn
  node_type          = "dax.t2.medium"
  replication_factor = 2
  server_side_encryption {
    enabled = true
  }
  subnet_group_name    = aws_dax_subnet_group.subnet_group.name
  security_group_ids   = [aws_security_group.dax-sg.id]
}
