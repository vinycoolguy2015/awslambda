From root module, run terragrunt apply-all.

The dependency block declares that the network folder configuration depends on the output from the Terraform configuration in the vpc folder. Terragrunt will recognize this and wait to apply this configuration until the configuration in the vpc folder has completed successfully during a terragrunt apply-all.

Keep in mind the terragrunt apply-all command should be used in the initial deployment of an environment. If you were to modify one infrastructure component, for example, the ec2 configuration, you would just run terragrunt apply in the ec2 directory to apply the change. 

After you are done, run terragrunt destroy-all
