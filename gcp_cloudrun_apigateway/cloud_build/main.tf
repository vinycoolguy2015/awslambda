resource "google_project_service" "build" {
  service            = "cloudbuild.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "registry" {
  service            = "containerregistry.googleapis.com"
  disable_on_destroy = false
}

resource "google_cloudbuild_trigger" "cloud_build_trigger" {
  name        = var.source_repo_name
  description = "Cloud Source Repository Trigger ${var.source_repo_name} (${var.branch_name})"
  trigger_template {
    repo_name   = var.source_repo_name
    branch_name = var.branch_name
  }
  filename   = "cloudbuild.yaml"
  depends_on = [google_project_service.build]
}

resource "null_resource" "empty_commit" {
  depends_on = [google_cloudbuild_trigger.cloud_build_trigger]
  provisioner "local-exec" {
    command = "cd /tmp/${var.source_repo_name}/ && git commit --allow-empty -m 'Trigger build' && git push origin master"
  }
}
