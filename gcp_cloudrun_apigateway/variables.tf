#define service account credentials
variable "gcp_auth_file" {
  type        = string
  description = "GCP authentication file"
}
# define GCP project name
variable "app_project" {
  type        = string
  description = "GCP project name"
}
# define GCP region
variable "gcp_region" {
  type        = string
  description = "GCP region"
}

#define source repo name
variable "source_repo_name" {
  type        = string
  description = "Google Cloud Source Repository Name"
}

variable "branch_name" {
  type = string
}


variable "image_name" {
  type        = string
  description = "image to be deployed on cloud run"
}
