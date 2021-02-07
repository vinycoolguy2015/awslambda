#!/bin/bash
  
basedir=$(pwd)
export terraform_provider_platform='darwin_amd64'
slack_url=''

for dir in $(find environments/qa -type d -maxdepth 2 -mindepth 2); do
  MESSAGE=''
  rm -rf /tmp/tf.plan
  printf  '\nChecking Directory: %s \n' "$dir" >> /tmp/test.txt
  cd $basedir/$dir
  terragrunt init -plugin-dir=$basedir/terraform_aws_plugins/plugins/darwin_amd64 #Change it to Linux one
  terragrunt plan  -out=/tmp/tf.plan
  if [ $? -ne 0 ];then
    MESSAGE="Terragrunt plan for $dir exited with non zero exit code.Please check issues with code."
  fi
  if terragrunt show -no-color /tmp/tf.plan| grep "#";then
    MESSAGE="Drift status for $dir\n\n"$(terragrunt show -no-color /tmp/tf.plan| awk '/#/,EOF { print $0 }');
  fi

  #Send message to Slack if MESSAGE is non-empty
  [[ ! -z "$MESSAGE" ]] && curl -X POST -H 'Content-type: application/json' --data "{'text':'$MESSAGE'}" $slack_url || echo "No changes detected"
done
