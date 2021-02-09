#!/bin/bash

#For testing only
export AWS_ACCESS_KEY_ID=''
export AWS_SECRET_ACCESS_KEY=''


export terraform_provider_platform='linux_amd64'
slack_url=''
MESSAGE=''

basedir=$(pwd)
for dir in $(find environments/gds-pdd-bgp.dev -type d -maxdepth 2 -mindepth 2); do
	cd $basedir/$dir
	rm -rf /tmp/tf.plan
	printf  '\nChecking Directory: %s \n' "$dir"
	terragrunt init
	terragrunt plan -out=/tmp/tf.plan
	if [ $? -ne 0 ];then
    	MESSAGE="Terragrunt plan for $dir exited with non zero exit code.Please check for code or permission related issues by executing terragrunt plan manually."
	else
		if terragrunt show -no-color /tmp/tf.plan| grep "#";then
    		MESSAGE="Drift status for $dir\n\n"$(terragrunt show -no-color /tmp/tf.plan| awk '/#/,EOF { print $0 }');
		fi
	fi
	[[ ! -z "$MESSAGE" ]] && curl -X POST -H 'Content-type: application/json' --data "{'text':'$MESSAGE'}" $slack_url || echo "No chnages detected"
done

#Now execute docker run --rm --name diff_checker -v `pwd`:/apps alpine/terragrunt:0.12.17 /bin/bash -c ' ./terraform_drift_check.sh'
