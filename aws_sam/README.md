Python version of https://aws.amazon.com/blogs/compute/implementing-safe-aws-lambda-deployments-with-aws-codedeploy/


sam package --template-file template.yaml --s3-bucket athena1989 --output-template-file packaged.yaml
sam deploy --template-file packaged.yaml --stack-name mySafeDeployStack --capabilities CAPABILITY_IAM
