FROM jenkins/jenkins:latest
USER root
RUN apt-get -y update && apt-get install -y wget apt-transport-https gnupg lsb-release &&\
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | apt-key add - &&\
echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main | tee -a /etc/apt/sources.list.d/trivy.list &&\
apt-get -y update  &&\
apt-get install -y trivy
RUN apt-get -y update && \
 apt-get -y install apt-transport-https ca-certificates curl gnupg-agent software-properties-common && \
 curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - && \
 add-apt-repository \
 "deb [arch=amd64] https://download.docker.com/linux/$(. /etc/os-release; echo "$ID") \
 $(lsb_release -cs) \
 stable" && \
 apt-get update && \
 apt-get -y install docker-ce docker-ce-cli containerd.io
