resource "aws_appmesh_mesh" "ecs_appmesh" {
  name = "jukebox-mesh"
  spec {
    egress_filter {
      type = "DROP_ALL"
    }
  }
}

resource "aws_appmesh_virtual_router" "metal" {
  name      = "metal-vr"
  mesh_name = aws_appmesh_mesh.ecs_appmesh.id
  spec {
    listener {
      port_mapping {
        port     = 80
        protocol = "http"
      }
    }
  }
}

resource "aws_appmesh_route" "metal_route" {
  name                = "metal-route"
  depends_on          = [aws_appmesh_virtual_router.metal, aws_appmesh_virtual_node.metal]
  mesh_name           = aws_appmesh_mesh.ecs_appmesh.id
  virtual_router_name = "metal-vr"

  spec {
    http_route {
      match {
        prefix = "/"
      }

      action {
        weighted_target {
          virtual_node = aws_appmesh_virtual_node.metal.name
          weight       = 1
        }


      }
    }
  }
}

resource "aws_appmesh_virtual_service" "metal" {
  name       = "${var.cloud_map_metal_service}.${var.cloud_map_namespace}"
  depends_on = [aws_appmesh_virtual_router.metal]
  mesh_name  = aws_appmesh_mesh.ecs_appmesh.id
  spec {
    provider {
      virtual_router {
        virtual_router_name = aws_appmesh_virtual_router.metal.name
      }
    }
  }
}

resource "aws_appmesh_virtual_service" "pop" {
  name       = "${var.cloud_map_pop_service}.${var.cloud_map_namespace}"
  depends_on = [aws_appmesh_virtual_node.pop]
  mesh_name  = aws_appmesh_mesh.ecs_appmesh.id
  spec {
    provider {
      virtual_node {
        virtual_node_name = aws_appmesh_virtual_node.pop.name
      }
    }
  }
}

resource "aws_appmesh_virtual_service" "jukebox" {
  name       = "${var.cloud_map_jukebox_service}.${var.cloud_map_namespace}"
  depends_on = [aws_appmesh_virtual_node.jukebox]
  mesh_name  = aws_appmesh_mesh.ecs_appmesh.id
  spec {
    provider {
      virtual_node {
        virtual_node_name = aws_appmesh_virtual_node.jukebox.name
      }
    }
  }
}

resource "aws_appmesh_virtual_node" "metal" {
  name      = "metal-service-vn"
  mesh_name = aws_appmesh_mesh.ecs_appmesh.id
  spec {
    listener {
      port_mapping {
        port     = 80
        protocol = "http"
      }
      health_check {
        protocol            = "http"
        path                = "/ping"
        healthy_threshold   = 2
        unhealthy_threshold = 2
        timeout_millis      = 2000
        interval_millis     = 5000
      }
    }
    service_discovery {
      aws_cloud_map {
        namespace_name = var.cloud_map_namespace
        service_name   = var.cloud_map_metal_service
      }
    }
  }
}

resource "aws_appmesh_virtual_node" "pop" {
  name      = "pop-service-vn"
  mesh_name = aws_appmesh_mesh.ecs_appmesh.id
  spec {
    listener {
      port_mapping {
        port     = 80
        protocol = "http"
      }
      health_check {
        protocol            = "http"
        path                = "/ping"
        healthy_threshold   = 2
        unhealthy_threshold = 2
        timeout_millis      = 2000
        interval_millis     = 5000
      }
    }
    service_discovery {
      aws_cloud_map {
        namespace_name = var.cloud_map_namespace
        service_name   = var.cloud_map_pop_service
      }
    }
  }
}

resource "aws_appmesh_virtual_node" "jukebox" {
  name       = "jukebox-service-vn"
  depends_on = [aws_appmesh_virtual_service.metal, aws_appmesh_virtual_service.pop]
  mesh_name  = aws_appmesh_mesh.ecs_appmesh.id
  spec {
    backend {
      virtual_service {
        virtual_service_name = "${var.cloud_map_metal_service}.${var.cloud_map_namespace}"
      }
    }
    backend {
      virtual_service {
        virtual_service_name = "${var.cloud_map_pop_service}.${var.cloud_map_namespace}"
      }
    }
    listener {
      port_mapping {
        port     = 9000
        protocol = "http"
      }
    }
    service_discovery {
      aws_cloud_map {
        namespace_name = var.cloud_map_namespace
        service_name   = var.cloud_map_jukebox_service
      }
    }
  }
}
