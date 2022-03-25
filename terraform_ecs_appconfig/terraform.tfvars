vpc_cidr                         = "10.6.0.0/16"
private_subnet                   = { count = 2, newbits = 10, netnum = 0 }
public_subnet                    = { count = 2, newbits = 10, netnum = 4 }
vpc_name                         = "ecs_vpc"
ecs_cluster_name                 = "fargate-cluster"
docker_container_port            = 80
ecs_service_name                 = "simplehttp"
docker_image_url                 = "8086.dkr.ecr.us-east-1.amazonaws.com/fastapi:latest"
memory                           = 512
desired_task_number              = 2
cpu                              = 256
env_name                         = "dev"
