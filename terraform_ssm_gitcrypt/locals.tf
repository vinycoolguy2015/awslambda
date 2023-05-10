locals {
  ssm_secure = merge(
    [
      for package, package_values in var.ssm_secure : {
        for k, v in package_values : "${package}/${k}" => v
      }
    ]...
  )
  }
