#!/bin/bash
gcloud beta filestore instances create jenkins-volume --zone=us-central1-a --tier=BASIC_HDD --file-share=name="jenkins",capacity=1TB --network=name="default"
ip=`gcloud filestore instances describe jenkins-volume --zone=us-central1-a| sed -n '/ipAddresses/{n;p;}' | tr -d ' '|cut -d "-" -f2`
gcloud compute ssh --zone us-central1-a centos@kubernetes-slave1 --command 'sudo yum -y update && sudo yum -y install nfs-utils'
gcloud compute ssh --zone us-central1-a centos@kubernetes-slave1 --command "sudo mkdir /mnt/jenkins && sudo mount -t nfs -o vers=3 $ip:/jenkins /mnt/jenkins && sudo chmod go+rw /mnt/jenkins"

gcloud compute ssh --zone us-central1-a centos@kubernetes-slave2 --command 'sudo yum -y update && sudo yum -y install nfs-utils'
gcloud compute ssh --zone us-central1-a centos@kubernetes-slave2 --command "sudo mkdir /mnt/jenkins && sudo mount -t nfs -o vers=3 $ip:/jenkins /mnt/jenkins && sudo chmod go+rw /mnt/jenkins"

gcloud compute ssh --zone us-central1-a centos@kubernetes-slave3 --command 'sudo yum -y update && sudo yum -y install nfs-utils'
gcloud compute ssh --zone us-central1-a centos@kubernetes-slave3 --command "sudo mkdir /mnt/jenkins && sudo mount -t nfs -o vers=3 $ip:/jenkins /mnt/jenkins && sudo chmod go+rw /mnt/jenkins"





