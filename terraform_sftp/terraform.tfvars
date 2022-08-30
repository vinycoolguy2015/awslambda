vpc_id             = "vpc-6a"
vpc_cidr           = "172.31.0.0/16"
subnet_ids         = ["subnet-0c0092", "subnet-0c1c88", "subnet-0ff0"]
sftp_users         = { internet = "internet" } # username is internet and home directory is also internet(inside the S3 bucket)
sftp_users_ssh_key = { internet = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC3CQYm+MgRVHiUYaNpnx4u4OvFMWDHnSiPw8iHWhgucBy4dpJ6bC6U4PCwLEb4NxaxHQw07fwQwqTo5vIXVjsfv0CK8mnvzxmPfxyyBH4SVeVOiEeIfRIucj0SFgUMrIZphtscCzt3JnwTVVpP1dkwWnPaeMx2+HdAMvF9lzvpYniJVSynAGoLvmbCZUK+WoKRXeMi3Gokr892HYhMktHwn5iUkIAd0UKbvzDQUn1DwMrbOhVUxgQup+nWYhnoK1NgKTBeSkLj8yVg9DgwUqNoeuoBKMQ4sTm0WT9Hlc4HCo1h2A+G099qMu4cY90Kb1LCz1UjyHZ8Yc9sKxw+Xy5BUNMu33XCwtgIU+aDgErxh6XdR20xzs6/LxfNcJAamrUssz/OfWGvnKarp3KYWDqx3EVUG/uGQb3hv8o1PKbVpfzbdsFsyiR3ymH7runJcG1FKDX+R9RklK/BnrTzZc4t }
