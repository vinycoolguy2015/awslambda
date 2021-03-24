**Solution for Ques 3 given at https://gist.github.com/houdinisparks/1e0fcdc9bb1c0d6d426e765ab6dc2abd:**

1- Install minikube as per the instructions provided at https://kubernetes.io/docs/tasks/tools/install-minikube/

2- Start minikube by executing minkube start comamnd

3- Download deployment yaml given at https://raw.githubusercontent.com/vinycoolguy2015/terraform_ansible/master/ques3/deployment.yaml

4- Apply this config using kubectl apply -f deployment.yaml

5- Check if pods are running using kubectl get pods command.

6- Execute minikube ip command and copy the ip provided by the output.

7- Open your browser and access url <minikube_ip:32042> and you'll see nginx page.
