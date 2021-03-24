**Solution for problem statement given at https://gist.github.com/houdinisparks/b8dcd1d2b5b1179b45b0afe68351e027:**

  1-Create EC2 IAM user with AmazonEC2FullAccess,AmazonRDSFullAccess and IAMFullAccess permission. Note down it's Access Key and Secret Access Key.

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
     
  
  6- Create a SSH key on base instance using ssh-keygen command with default parameters.

  7- Clone code repo using git clone https://github.com/vinycoolguy2015/terraform_ansible

  8- cd terraform_ansible/ques4/terraform_files

  9- Execute following commands to create our infrastructure:
  
  
        terraform init
        terraform plan
        terraform apply
        
  10- Once terraform apply completes, it will output the DNS of the ALB created. Hit that URL in your browser and you'll see node application's home page
  
  **Known Issue: As per https://github.com/chapagain/nodejs-mysql-crud, we need to create a table named users. This process is manual. We need to create a temporary bastion server to ssh into webserver instance.Once we are logged in to webserver, we can connect to RDS and create this table ** 
  
 
  
