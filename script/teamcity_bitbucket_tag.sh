#!/bin/bash
#Fetch commit message for this commit id
commit_message=$(git log --format=%B -n 1 $COMMIT_ID)

#Fetch last tag
last_tag=$(git describe --tags --abbrev=0)
major_version=$(echo $last_tag | cut -d '.' -f1 |cut -d 'v' -f2)
minor_version=$(echo $last_tag | cut -d '.' -f2)
patch_version=$(echo $last_tag | cut -d '.' -f3)
#Check if current commit is MAJOR/MINOR/PATCH
shopt -s nocasematch
case $commit_message in
  *\[Major\]*)
    major_version=`expr $major_version + 1`
    minor_version=0
    patch_version=0
    ;;
  *\[Minor\]*)
    minor_version=`expr $minor_version + 1`
    patch_version=0
    ;;
  *\[PATCH\]*)
    patch_version=`expr $patch_version + 1`
    ;;
  *)
    echo "Could not determine whether this commit is a Major/Minor or Patch"
    exit 1
    ;;
esac
new_tag=v"$major_version.$minor_version.$patch_version.$BRANCH_NAME"
echo "new tag will be $new_tag"
echo "##teamcity[setParameter name='env.NEW_TAG' value='"$new_tag"']"

#Add these environment variables in Teamcity build config
#COMMIT_ID: %system.build.vcs.number%
#NEW_TAG: Leave it as empty as we’ll populate it dynamically during build step.
#BRANCH_NAME: %teamcity.build.branch%
