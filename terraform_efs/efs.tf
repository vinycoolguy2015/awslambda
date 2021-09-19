resource "aws_efs_file_system" "efs" {
   creation_token = "efs"
   performance_mode = "generalPurpose"
   throughput_mode = "bursting"
   encrypted = "true"
 tags = {
     Name = "EFS"
   }
 }

resource "aws_efs_backup_policy" "policy" {
  file_system_id = aws_efs_file_system.efs.id
  backup_policy {
    status = "ENABLED"
  }
}

resource "aws_efs_mount_target" "efs-mt" {
   count = length(data.aws_availability_zones.available.names)
   file_system_id  = aws_efs_file_system.efs.id
   subnet_id = aws_subnet.subnet[count.index].id
   security_groups = [aws_security_group.efs.id]
 }
