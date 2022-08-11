#! /bin/bash
mv -f params.encrypted params.encrypted.$(date '+D%Y%m%d-T%H%M%S')
aws kms encrypt --key-id alias/ssm --region us-east-1 --plaintext fileb://params.decrypted --output text --query CiphertextBlob > params.encrypted
