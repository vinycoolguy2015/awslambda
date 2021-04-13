#!/bin/bash

generate_new_access_key() {
users=$(aws iam list-users|jq --raw-output '.Users[]|.UserName')
for user in $users; do
  echo "Creating a new access key for $user"
  active_keys=$(aws iam list-access-keys --user-name "$user"| jq '.AccessKeyMetadata|length')
  if [ "$active_keys" == "2" ]
  then
    echo "The user already has 2 set of access keys.Can't create another access key"
   else
    aws iam create-access-key --user-name "$user"
  fi
done

}

if [ -z "$1" ]
  then
    echo "Do you wish to generate a new access key for all the users?"
    select yn in "Yes" "No"; do
    case $yn in
        Yes ) generate_new_access_key; break;;
        No ) echo "Exiting";exit;;
    esac
done
else
  active_keys=$(aws iam list-access-keys --user-name "$1"| jq '.AccessKeyMetadata|length')
  if [ "$active_keys" == "2" ]
  then
    echo "The user already has 2 set of access keys.Can't create another access key"
   else
   aws iam create-access-key --user-name "$1"
fi
fi
