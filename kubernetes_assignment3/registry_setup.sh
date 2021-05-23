#!/bin/bash
sudo mkdir -p /registry && cd /registry && sudo mkdir certs
sudo openssl req -x509 -newkey rsa:4096 -days 365 -nodes -sha256 -keyout certs/tls.key -out certs/tls.crt -subj "/CN=docker-registry"
sudo mkdir auth
sudo sh -c 'docker run --rm --entrypoint htpasswd registry:2.6.2 -Bbn myuser mypasswd > auth/htpasswd'
sudo kubectl create ns registry
sudo kubectl create secret -n registry tls certs-secret --cert=/registry/certs/tls.crt --key=/registry/certs/tls.key
sudo kubectl create secret -n registry generic auth-secret --from-file=/registry/auth/htpasswd
sudo kubectl apply -f ~/registry.yaml


REGISTRY_IP=`sudo kubectl describe svc docker-registry | grep IPs | cut -d ":" -f2| tr -d " "`
echo $REGISTRY_IP > /tmp/ip.txt
