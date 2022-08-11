#! /bin/bash
mv -f params.decrypted params.decrypted.$(date '+D%Y%m%d-T%H%M%S')
aws kms decrypt --ciphertext-blob fileb://<(cat params.encrypted | base64 -d) --output text --query Plaintext --region us-east-1 | base64 --decode > params.decrypted
