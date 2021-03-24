resource "aws_db_instance" "application" {
  allocated_storage       = var.db_storage
  storage_type            = "gp2"
  engine                  = "mysql"
  engine_version          = "5.7"
  instance_class          = var.dbinstance_class
  name                    = "test"
  identifier              =  var.rds_name
  username                =  var.dbuser
  password                = var.dbpassword
  skip_final_snapshot     = true
  parameter_group_name    = "default.mysql5.7"
  db_subnet_group_name    = var.dbsubnet
  multi_az                = true
  storage_encrypted       = true
  vpc_security_group_ids  = var.rds_security_group
  tags = {
    Name = var.rds_name
  }
}

