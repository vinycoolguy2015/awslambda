Follow https://dev.to/heroku/how-to-manage-your-secrets-with-git-crypt-56ih to store terraform.tfvars in encrypted format

cat .gitattributes 
terraform.tfvars filter=git-crypt diff=git-crypt
