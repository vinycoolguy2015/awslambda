#Parameters
project='second-inquiry-309710'

#Targets
create-kubernetes-cluster:

	#Update firewall rule
	gcloud config set project $(project)
	gcloud compute firewall-rules update default-allow-internal --allow all

	#Create instances
	gcloud compute instances create --machine-type=n1-standard-2 --image-family=centos-7 --image-project=centos-cloud kubernetes-master1 kubernetes-master2 kubernetes-slave1 kubernetes-slave2 kubernetes-slave3 --zone us-central1-a

	#Create host entries
	chmod +x ./host_entries.sh
	./host_entries.sh
	sleep 30

	#Setup password less authentication
	gcloud compute ssh --zone us-central1-a centos@kubernetes-master1 --command 'ssh-keygen -t rsa -N "" -f .ssh/id_rsa'
	gcloud compute ssh --zone us-central1-a centos@kubernetes-master1 --command 'cat .ssh/id_rsa.pub >> .ssh/authorized_keys'
	gcloud compute scp --zone us-central1-a centos@kubernetes-master1:/home/centos/.ssh/id_rsa.pub /tmp

	gcloud compute scp --zone us-central1-a /tmp/id_rsa.pub centos@kubernetes-master2:/tmp
	gcloud compute scp --zone us-central1-a /tmp/id_rsa.pub centos@kubernetes-slave1:/tmp
	gcloud compute scp --zone us-central1-a /tmp/id_rsa.pub centos@kubernetes-slave2:/tmp
	gcloud compute scp --zone us-central1-a /tmp/id_rsa.pub centos@kubernetes-slave3:/tmp

	gcloud compute ssh --zone us-central1-a centos@kubernetes-master2 --command 'cat /tmp/id_rsa.pub >> .ssh/authorized_keys'
	gcloud compute ssh --zone us-central1-a centos@kubernetes-slave1 --command 'cat /tmp/id_rsa.pub >> .ssh/authorized_keys'
	gcloud compute ssh --zone us-central1-a centos@kubernetes-slave2 --command 'cat /tmp/id_rsa.pub >> .ssh/authorized_keys'
	gcloud compute ssh --zone us-central1-a centos@kubernetes-slave3 --command 'cat /tmp/id_rsa.pub >> .ssh/authorized_keys'

	#Setup Ansible
	gcloud compute ssh --zone us-central1-a centos@kubernetes-master1 --command 'sudo gpasswd -a centos wheel && sudo service firewalld stop && sudo setenforce 0 && sudo yum install -y epel-release git python-pip'
	gcloud compute ssh --zone us-central1-a centos@kubernetes-slave1 --command 'sudo gpasswd -a centos wheel && sudo service firewalld stop && sudo setenforce 0'
	gcloud compute ssh --zone us-central1-a centos@kubernetes-slave2 --command 'sudo gpasswd -a centos wheel && sudo service firewalld stop && sudo setenforce 0'
	gcloud compute ssh --zone us-central1-a centos@kubernetes-slave3 --command 'sudo gpasswd -a centos wheel && sudo service firewalld stop && sudo setenforce 0'
	gcloud compute ssh --zone us-central1-a centos@kubernetes-master2 --command 'sudo gpasswd -a centos wheel && sudo service firewalld stop && sudo setenforce 0'
	gcloud compute ssh --zone us-central1-a centos@kubernetes-master1 --command 'git clone https://github.com/kubernetes-sigs/kubespray.git'
	gcloud compute ssh --zone us-central1-a centos@kubernetes-master1 --command 'cd kubespray && sed -i "/helm_enabled: false/c\helm_enabled: true" roles/kubernetes-apps/helm/defaults/main.yml && sudo pip install -r requirements.txt && cp -rfp inventory/sample inventory/mycluster && echo "helm_enabled: true" >>inventory/mycluster/group_vars/k8s_cluster/k8s-cluster.yml'
	gcloud compute scp --zone us-central1-a hosts.ini centos@kubernetes-master1:/home/centos/kubespray/inventory/mycluster/
	
	#Create Cluster
	gcloud compute ssh --zone us-central1-a centos@kubernetes-master1 --command 'cd kubespray && ansible-playbook -i inventory/mycluster/hosts.ini --become --become-user=root --key-file=~/.ssh/id_rsa cluster.yml'
	gcloud compute ssh --zone us-central1-a centos@kubernetes-master1 --command 'sudo cp /etc/kubernetes/admin.conf /tmp && sudo chown centos:centos /tmp/admin.conf'
	mkdir ~/.kube
	gcloud compute scp --zone us-central1-a centos@kubernetes-master1:/tmp/admin.conf ~/.kube/

	#Create Jenkins Volume
	chmod +x ./create_jenkins_volume.sh 
	./create_jenkins_volume.sh

	#Install Istio
	gcloud compute scp --zone us-central1-a install_istio.sh centos@kubernetes-master1:/home/centos
	gcloud compute ssh --zone us-central1-a centos@kubernetes-master1 --command 'chmod +x /home/centos/install_istio.sh && /home/centos/install_istio.sh'
	gcloud compute ssh --zone us-central1-a centos@kubernetes-master1 --command 'sudo kubectl create ns development && sudo /home/centos/istio-1.6.6/bin/istioctl install --set profile=demo && sudo kubectl label namespace development istio-injection=enabled'

	#Install Nginx Ingress Controller
	gcloud compute ssh --zone us-central1-a centos@kubernetes-master1 --command 'sudo kubectl create namespace nginx-ingress-controller && sudo helm repo add stable https://charts.helm.sh/stable/ && sudo helm repo update && sudo helm install nginx-ingress-controller stable/nginx-ingress -n nginx-ingress-controller'

	#Install Kubernetes Dashboard With Read Only Token
	gcloud compute scp --zone us-central1-a *.yaml centos@kubernetes-master1:/home/centos
	gcloud compute ssh --zone us-central1-a centos@kubernetes-master1 --command 'sudo kubectl apply -f metric_server.yaml && sudo kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0/aio/deploy/recommended.yaml && sudo kubectl apply -f dashboard.yaml'

	#Install Jenkins
	gcloud compute ssh --zone us-central1-a centos@kubernetes-master1 --command 'sudo kubectl apply -f jenkins.yaml'

	#Registry setup
	gcloud compute scp --zone us-central1-a registry_setup.sh centos@kubernetes-master1:/home/centos
	gcloud compute ssh --zone us-central1-a centos@kubernetes-master1 --command 'chmod +x /home/centos/registry_setup.sh && /home/centos/registry_setup.sh' 
	gcloud compute scp --zone us-central1-a centos@kubernetes-master1:/tmp/ip.txt /tmp/ip.txt
	gcloud compute scp --zone us-central1-a centos@kubernetes-master1:/registry/certs/tls.crt /tmp/tls.crt
	IP=`cat /tmp/ip.txt`
	gcloud compute ssh --zone us-central1-a centos@kubernetes-slave1 --command 'sudo mkdir -p /etc/docker/certs.d/docker-registry:5000'
	gcloud compute ssh --zone us-central1-a centos@kubernetes-slave2 --command 'sudo mkdir -p /etc/docker/certs.d/docker-registry:5000'
	gcloud compute ssh --zone us-central1-a centos@kubernetes-slave3 --command 'sudo mkdir -p /etc/docker/certs.d/docker-registry:5000'
	gcloud compute ssh --zone us-central1-a centos@kubernetes-slave1 --command "sudo sed -i \"$ a $IP docker-registry\" /etc/hosts"
	gcloud compute ssh --zone us-central1-a centos@kubernetes-slave2 --command "sudo sed -i \"$ a $IP docker-registry\" /etc/hosts"
	gcloud compute ssh --zone us-central1-a centos@kubernetes-slave3 --command "sudo sed -i \"$ a $IP docker-registry\" /etc/hosts"
	gcloud compute scp --zone us-central1-a /tmp/tls.crt centos@kubernetes-slave1:/tmp/ca.crt
	gcloud compute scp --zone us-central1-a /tmp/tls.crt centos@kubernetes-slave2:/tmp/ca.crt
	gcloud compute scp --zone us-central1-a /tmp/tls.crt centos@kubernetes-slave3:/tmp/ca.crt
	gcloud compute ssh --zone us-central1-a centos@kubernetes-slave1 --command 'sudo cp /tmp/ca.crt /etc/docker/certs.d/docker-registry:5000/ca.crt'
	gcloud compute ssh --zone us-central1-a centos@kubernetes-slave2 --command 'sudo cp /tmp/ca.crt /etc/docker/certs.d/docker-registry:5000/ca.crt'
	gcloud compute ssh --zone us-central1-a centos@kubernetes-slave3 --command 'sudo cp /tmp/ca.crt /etc/docker/certs.d/docker-registry:5000/ca.crt'

	#Application Setup
	gcloud compute scp --recurse --zone us-central1-a app_deployment centos@kubernetes-master1:/home/centos
        gcloud compute ssh --zone us-central1-a centos@kubernetes-master1 --command 'sudo kubectl apply -f app_deployment/'
