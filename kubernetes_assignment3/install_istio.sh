#!/bin/bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" 
chmod +x ./kubectl
sudo mv kubectl /usr/bin
sudo cp /usr/local/bin/helm /usr/bin/helm
sudo chmod +x /usr/bin/helm
curl -L https://istio.io/downloadIstio | ISTIO_VERSION=1.6.6 sh - 
cd istio-1.6.6
echo "export PATH=$PWD/bin:$PATH" >> ~/.bash_profile
