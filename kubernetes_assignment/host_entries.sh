#! /bin/bash

kubernetes_master1_ip=`gcloud compute instances describe kubernetes-master1 --zone us-central1-a --format='get(networkInterfaces[0].networkIP)'`
kubernetes_master2_ip=`gcloud compute instances describe kubernetes-master2 --zone us-central1-a --format='get(networkInterfaces[0].networkIP)'`
kubernetes_slave1_ip=`gcloud compute instances describe kubernetes-slave1 --zone us-central1-a --format='get(networkInterfaces[0].networkIP)'`
kubernetes_slave2_ip=`gcloud compute instances describe kubernetes-slave2 --zone us-central1-a --format='get(networkInterfaces[0].networkIP)'`
kubernetes_slave3_ip=`gcloud compute instances describe kubernetes-slave3 --zone us-central1-a --format='get(networkInterfaces[0].networkIP)'`

cat <<EOF > hosts.ini
[all]
node1 ansible_host=$kubernetes_master1_ip
node2 ansible_host=$kubernetes_master2_ip
node3 ansible_host=$kubernetes_slave1_ip
node4 ansible_host=$kubernetes_slave2_ip
node5 ansible_host=$kubernetes_slave3_ip
[kube-master]
node1
node2
[etcd]
node1
node2
node3
[kube-node]
node3
node4
node5
[k8s-cluster:children]
kube-master
kube-node
EOF
