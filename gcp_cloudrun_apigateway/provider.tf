terraform {
  required_version = ">= 0.12"
}
provider "google" {
  project     = var.app_project
  credentials = file(var.gcp_auth_file)
  region      = var.gcp_region
}

provider "google-beta" {
  project = var.app_project
  region  = var.gcp_region
}
