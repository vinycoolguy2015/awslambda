terraform {
  source = "../modules/ssm"

  # Remember to set ANSIBLE_VAULT_PASSWORD_FILE
  before_hook "vault_decrypt" {
    commands     = ["apply", "plan", "init","destroy"]
    execute      = ["ansible-vault", "decrypt", "terraform.tfvars"]
    run_on_error = false
  }
  after_hook "vault_remove_secret" {
    commands     = ["apply", "plan", "init","destroy"]
    execute      = ["rm", "terraform.tfvars"]
    run_on_error = false
  }
}
