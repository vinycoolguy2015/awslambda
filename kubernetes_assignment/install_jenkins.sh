#/bin/bash
gcloud compute ssh --zone us-central1-a centos@jenkins --command 'sudo yum install -y java-1.8.0-openjdk-devel wget &&\
                sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat/jenkins.repo &&\
                sudo rpm --import https://pkg.jenkins.io/redhat/jenkins.io.key &&\
                sudo yum install -y jenkins git docker &&\
                sudo systemctl enable jenkins &&\
                sudo systemctl enable docker &&\
                sudo systemctl start docker &&\
                sudo groupadd docker &&\
                sudo chown -R root:docker /var/run/docker.sock &&\
                sudo usermod -aG docker jenkins &&\
                sudo systemctl restart docker &&\
                sudo systemctl start jenkins &&\
		sleep 15 && echo "Jenkins password is: " && sudo cat /var/lib/jenkins/secrets/initialAdminPassword' 
