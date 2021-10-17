resource "aws_kms_key" "ecr_kms" {
  description             = "KMS Key For ECR"
  deletion_window_in_days = 30
}

resource "aws_ecr_repository" "ecr_repo" {
  name                 = "ecr_repo"
  image_tag_mutability = var.tag_mutability
  encryption_configuration {
    encryption_type = "KMS"
    kms_key         = aws_kms_key.ecr_kms.arn
  }
  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_lifecycle_policy" "ecr_repo_policy" {
  repository = aws_ecr_repository.ecr_repo.name
  policy     = <<EOF
{
    "rules": [
        {
            "rulePriority": 1,
            "description": "Keep last n images",
            "selection": {
                "tagStatus": "tagged",
                "tagPrefixList": ["v"],
                "countType": "imageCountMoreThan",
                "countNumber": ${var.image_count}
            },
            "action": {
                "type": "expire"
            }
        }
    ]
}
EOF
}
