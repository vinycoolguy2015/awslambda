#!/bin/bash
ip=$(gcloud compute instances describe kubernetes-master1 --zone us-central1-a --format='get(networkInterfaces[0].networkIP)')
sed -i "s/127.0.0.1/$ip/g" ~/.kube/admin.conf
gcloud compute scp --zone us-central1-a ~/.kube/admin.conf  centos@jenkins:/home/centos/
gcloud compute ssh --zone us-central1-a centos@jenkins --command 'curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 > get_helm.sh &&\
                chmod 700 get_helm.sh &&\
                sudo yum install -y openssl &&\
                ./get_helm.sh &&\
                sudo mkdir /var/lib/jenkins/.kube &&\
                sudo mv admin.conf /var/lib/jenkins/.kube/config &&\
                sudo chown -R jenkins:jenkins /var/lib/jenkins/.kube'
