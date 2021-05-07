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
	
	#Install EFK
	gcloud compute scp --zone us-central1-a --recurse efk/ centos@kubernetes-master1:/home/centos/
	gcloud compute ssh --zone us-central1-a centos@kubernetes-master1 --command 'cd /home/centos/efk && sudo cp /usr/local/bin/helm /usr/bin/helm && sudo cp /usr/local/bin/kubectl /usr/bin/kubectl && sudo kubectl apply -f kube-logging.yaml && sudo kubectl apply -f elasticsearch_svc.yaml && sudo kubectl apply -f elasticsearch_statefulset.yaml && sudo kubectl apply -f kibana.yaml && sudo kubectl apply -f fluentd.yaml'
	
	#Install Grafana and Prometheus
	gcloud compute ssh --zone us-central1-a centos@kubernetes-master1 --command 'sudo helm repo add stable https://charts.helm.sh/stable && sudo helm repo update && sudo kubectl create ns monitoring && sudo helm install prometheus stable/prometheus-operator --namespace monitoring'
	gcloud compute ssh --zone us-central1-a centos@kubernetes-master1 --command 'echo "Note down Grafana password." && sudo kubectl get secret --namespace monitoring prometheus-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo'
	
	#Setup guestbook application
	gcloud compute scp --zone us-central1-a --recurse guestbook-deployment/ centos@kubernetes-master1:/home/centos/
	gcloud compute ssh --zone us-central1-a centos@kubernetes-master1 --command 'cd /home/centos && sudo helm install guestbook --create-namespace --namespace=development ./guestbook-deployment/'
	
	#Install Jenkins
	gcloud compute firewall-rules create jenkins --allow=tcp:8080 --description="Allow access to Jenkins" --direction=INGRESS --target-tags='jenkins' --source-ranges='0.0.0.0/0'
	gcloud compute instances create --machine-type=n1-standard-2 --image-family=centos-7 --image-project=centos-cloud jenkins --zone us-central1-a --tags='jenkins'
	./install_jenkins.sh
	        
	#Setup helm on Jenkins server
	./setup_helm_on_jenkins.sh

