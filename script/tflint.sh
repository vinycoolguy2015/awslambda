#!/bin/bash

set -u
set -o pipefail

yell() { echo "$0: $*" >&2; }
die() { yell "$*"; exit 111; }
try() { "$@" || die "cannot $*"; }

TFLINT_VERSION=${TFLINT_VERSION:-0.24.1}
TF_VERSION=${TF_VERSION:-0.13.6}
TFLINT_CONFIG=$(cat .tflint.hcl)

#docker pull wata727/tflint:${TFLINT_VERSION}
docker pull ghcr.io/terraform-linters/tflint:latest
# docker pull hashicorp/terraform:${TF_VERSION:-0.12.7}
docker pull alpine/terragrunt:${TF_VERSION} # includes terragrunt

export exit_status=0

# check ./modules dir
for dir in $(find modules ! -path modules -type d); do
  printf  '\nChecking Directory: %s \n' "$dir"
  echo  "| TFLINT CHECK: directory: $dir |"
  echo "$TFLINT_CONFIG" > .tflint_config
  docker run --rm  --workdir /data -v $(pwd):/data ghcr.io/terraform-linters/tflint:latest --config .tflint_config $dir || { exit_status=$?; printf "tflint check has failed. \n"; }
  rm .tflint_config
  # echo "exit status in TFLINT if $exit_status"
    
  echo  "| FORMATTING CHECK: directory: $dir |"
  docker run --rm  --entrypoint terraform -v $(pwd):/apps alpine/terragrunt:${TF_VERSION} fmt --check /apps/$dir || { exit_status=$?;  printf "formating check has failed. \n"; }
  # echo "exit status in FORMATTING if $exit_status"
  # echo "exit status in loop $?"s
done

# check ./environments dir
docker run --rm --entrypoint terragrunt -w /apps/environment -v $(pwd):/apps \
alpine/terragrunt:${TF_VERSION} hclfmt --terragrunt-check || { exit_status=$?;  printf "formating check has failed. \n"; }

docker run --rm  --entrypoint terraform -w /apps -v $(pwd):/apps \
alpine/terragrunt:${TF_VERSION} fmt --recursive --check /apps/environments || { exit_status=$?;  printf "formating check has failed. \n"; }

#SAST scanning
docker run --rm -it -v "$(pwd):/environment" tfsec/tfsec /environment || { exit_status=$?;  printf "SAST check has failed. \n"; }

if [[ $exit_status -ne 0 ]]; then
  printf "Terraform checks has failed. Exiting.\n"
  exit 1
else
  printf "Terraform checks has passed. HOORAY!.\n"
  exit 0
fi
