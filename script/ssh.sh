#!/bin/bash

input="user.txt"
server1=x.x.x.x
server2=x.x.x.x
password=password.txt
default_user_password="user_password@2020#"

#Function to copy ssh keys from server1
copy_ssh_key() {
  echo "Checking if ssh key exists for $user on $server1 so that we can copy it to $server2"
  sshpass -f $password ssh -n -o StrictHostKeyChecking=no $server1 "sudo test -f /home/${user}/.ssh/authorized_keys"
  if [ $? -eq 0 ];then
    echo "Copying ssh key for $user from $server1 to $server2"
    sshpass -f $password ssh -n -o StrictHostKeyChecking=no $server1 "sudo cp /home/${user}/.ssh/authorized_keys /tmp/${user}_authorized_keys && sudo chmod 777 /tmp/${user}_authorized_keys"
    sshpass -f $password scp ${server1}:/tmp/${user}_authorized_keys /tmp
    sshpass -f $password ssh -n -o StrictHostKeyChecking=no $server1 "sudo rm -rf /tmp/${user}_authorized_keys"
    sudo cp /tmp/${user}_authorized_keys /home/${user}/.ssh/authorized_keys && sudo chmod 600 /home/${user}/.ssh/authorized_keys && sudo chown ${user}:${user} /home/${user}/.ssh/authorized_keys && sudo rm -rf /tmp/${user}_authorized_keys
    sudo test -f /home/${user}/.ssh/authorized_keys
    if [ $? -eq 0 ];then
      echo "Successfully copied ssh key for $user from $server1 to $server2"
    else
      echo "Error copying ssh key for $user from $server1 to $server2"
    fi
  else
    echo "SSH key for $user does not exist on $server1.Creating $user on $server2 with password authentication "
    echo -e "${default_user_password}\n${default_user_password}" |sudo passwd $user
  fi
}


#Looping through the list of users
while IFS= read -r user
do
  echo "Checking user $user on $server2"
  grep $user /etc/passwd
  if [ $? -eq 0 ];then
    echo "User $user already exists on $server2. Checking whether authorized_keys exists or not"
    sudo test -f /home/$user/.ssh/authorized_keys
    if [ $? -eq 0 ];then
      echo "User $user on $server2 already has authorized_keys file available.No action required."
    else
      echo "Checking whether /home/$user exists in $server2."
      sudo test -d /home/$user/
      if [ $? -eq 0 ];then
        echo "/home/$user exists in $server2.Now checking if .ssh directory is available"
        sudo test -d /home/$user/.ssh
        if [ $? -eq 0 ];then
          echo ".ssh directory for $user exists on $server2.Copying ssh key from $server1"
          copy_ssh_key
        else
          echo "/home/$user/.ssh does not exist. Creating .ssh for $user on $server2"
          sudo mkdir /home/$user/.ssh && sudo chown -R ${user}:${user} /home/${user}  && sudo chmod 700 /home/${user}
          copy_ssh_key
        fi
      else
        echo "Creating home and .ssh directory for $user on $server2."
        sudo mkdir -p /home/$user/.ssh && sudo chown -R ${user}:${user} /home/${user}  && sudo chmod 700 /home/${user}
        copy_ssh_key
      fi
    fi
  else
    echo "Creating user ${user}"
    sudo adduser ${user} && sudo mkdir /home/${user}/.ssh
    sudo chown -R ${user}:${user} /home/${user}/.ssh  && sudo chmod 700 /home/${user}/.ssh
    copy_ssh_key
  fi
done < "$input"
