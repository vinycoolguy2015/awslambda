**Solution for Ques 1 and Ques 2 given at https://gist.github.com/houdinisparks/1e0fcdc9bb1c0d6d426e765ab6dc2abd:**

  1-Create EC2 IAM user with AmazonEC2FullAccess permission. Note down it's Access Key and Secret Access Key.

  2-Launch a CentOS 7 machine in AWS and SSH into that machine.This will act as a base instance where we'll execute our script

  3-Execute following commands on our base instance:  
  
      
      sudo yum update -y  
      sudo yum install -y git wget unzip epel-release   
      sudo yum install -y python-pip  
      sudo pip install awscli  
      

  4-Setup AWS CLI on base instance using aws configure command and set following parameters:  
    
    AWS Access Key ID : <access_key_of_IAM_user_we_created in step 1>  
    AWS Secret Access Key : <secret_access_key_of_IAM_user_we_created in step 1>  
    Default region name : us-east-1]
   
 
  5- Setup Terraform on base instance using following commands: 
  
  
    wget https://releases.hashicorp.com/terraform/0.12.28/terraform_0.12.28_linux_amd64.zip
    unzip terraform_0.12.28_linux_amd64.zip 
    sudo mv terraform /usr/local/bin
     
  6- Install ansible on base instance using sudo yum install -y ansible command. Open /etc/ansible/ansible.cfg and uncomment host_key_checking = False to disable        host checking.
  
  7- Create a SSH key on base instance using ssh-keygen command with default parameters.

  8- Clone code repo using git clone https://github.com/vinycoolguy2015/terraform_ansible

  9- cd terraform_ansible/ques1_ques2/terraform_files

  10- Execute following commands to create our infrastructure:
  
  
        terraform init
        terraform plan
        terraform apply
        
  11- Once terraform apply completes, it will output the IP of the instance terraform created. From base instance, SSH into that instance.
  
  
  ```
  ssh -i ~/.ssh/id_rsa ec2-user@<IP Given by Terraform output>
  ```
  
  12- Now for Ques2 deliverables, run following commnds on the newly created instance:
  
  
  ```
  nslookup www.google.com
  curl https://www.google.com
  telnet localhost 80
  telnet localhost 8080
  telnet localhost 3306
  ```
  
  
  
