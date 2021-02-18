#!/bin/bash
git tag -l | xargs -n 1 git push --delete origin #Delete from repo
git tag | xargs git tag -d # delete locally
