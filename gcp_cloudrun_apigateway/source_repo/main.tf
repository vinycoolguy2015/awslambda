resource "google_project_service" "repo" {
  service            = "sourcerepo.googleapis.com"
  disable_on_destroy = false
}


resource "google_sourcerepo_repository" "my-repo" {
  name = var.source_repo_name
  depends_on=[google_project_service.repo]
  provisioner "local-exec" {
    command = "cd /tmp && rm -rf ${var.source_repo_name} && gcloud source repos clone ${var.source_repo_name} && cd ${var.source_repo_name} && cp -R ~/gcp_cloudrun_apigateway/code/* . && git add * && git commit -m 'Initial commit' && git push -u origin master"
  }
}
