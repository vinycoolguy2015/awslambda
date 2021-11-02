vpc_cidr              = "10.6.0.0/16"
private_subnet        = { count = 2, newbits = 10, netnum = 0 }
public_subnet         = { count = 2, newbits = 10, netnum = 4 }
vpc_name              = "ecs_vpc"
ecs_cluster_name      = "fargate-cluster"
docker_container_port = 9000
