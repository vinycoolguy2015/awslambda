
module "source_repo" {
  source           = "./source_repo"
  source_repo_name = var.source_repo_name
}

module "cloud_build" {
  source           = "./cloud_build"
  source_repo_name = var.source_repo_name
  branch_name      = var.branch_name
  depends_on       = [module.source_repo]
}

module "cloud_run" {
  source           = "./cloud_run"
  image_name       = var.image_name
  gcp_region       = var.gcp_region
  source_repo_name = var.source_repo_name
  depends_on       = [module.cloud_build]
}

module "api_gateway" {
  source     = "./api_gateway"
  region     = var.gcp_region
  depends_on = [module.cloud_run]
}

