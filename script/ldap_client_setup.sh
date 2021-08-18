#!/bin/bash

ldap_ip=172.31.32.184
checkSSHD_cmd=$(grep "AuthorizedKeysCommand " /etc/ssh/sshd_config | cut -c1-1)
checkSSHD_cmdUser=$(grep "AuthorizedKeysCommandUser" /etc/ssh/sshd_config | cut -c1-1)
ldapSSHscript="ldap-ssh.sh"
ldapSSHscriptPath=/usr/local/bin
checkPamAuth=$(grep "^auth" /etc/pam.d/su | grep -c "pam_succeed_if.so")
arg1=$1

usage() {
cat << EOF
Usage: $0
$0 users           Description: Setup ldap client with users config
$0 admin           Description: Setup ldap client with admin config

EOF
exit;
}

chkError() {
  if [ "$?" -ne 0 ]; then
    echo"Error occurred, please verify before proceeding"
    exit
  fi
}

if [[ "$arg1" != "users" ]] && [[ "$arg1" != "admin" ]]; then
  usage
fi

if [[ "$arg1" == "users" ]]; then
  group="wheel"
elif [[ "$arg1" == "admin" ]]; then
  group="admin"
fi

if [[ "$USER" != "root" ]]; then
  echo "Installation can only be done by root"
  exit
fi

osVersion=$(awk '{print $1}' /etc/redhat-release)


if [[ "$osVersion" != "CentOS" ]]; then
  echo "This script is only meant to be used on centos"
  exit
fi

#Installing openldap clients
yum -y install openldap openldap-clients nss-pam-ldapd

# Config to point to ldap server
authconfig --enableldap --enableldapauth --ldapserver="$ldap_ip" --ldapbasedn="dc=example,dc=com" --enablemkhomedir --update

# Copy ldap ssh pub key script to /usr/local/bin
cp "$ldapSSHscript" "$ldapSSHscriptPath"
chmod 755 "$ldapSSHscriptPath"/"$ldapSSHscript"

# Modify sshd_config to support public key from ldap
if [[ "$checkSSHD_cmd" == "" ]] || [[ "$checkSSHD_cmd" == "#" ]]; then
  sed -i '/AuthorizedKeysCommand /c\AuthorizedKeysCommand /usr/local/bin/ldap-ssh.sh' /etc/ssh/sshd_config
else
  echo "AuthorizedKeysCommand already configured, please verify"
fi

if [[ "$checkSSHD_cmdUser" == "" ]] || [[ "$checkSSHD_cmdUser" == "#" ]]; then
  sed -i '/AuthorizedKeysCommandUser/c\AuthorizedKeysCommandUser nobody' /etc/ssh/sshd_config
else
  echo "AuthorizedKeysCommandUser already configured, please verify"
fi

# Restart sshd daemon
systemctl restart sshd

# Update sudoer to allow nopass to wheel group
checkSudoer=$(grep "NOPASSWD" /etc/sudoers | grep "$group" | cut -c1-1)

configWheelSudo() {
  if [[ "$checkSudoer" == "" ]] || [[ "$checkSudoer" == "#" ]]; then
    sed -i '/wheel.*NOPASSWD/c\%wheel  ALL=(ALL)       NOPASSWD: ALL' /etc/sudoers
  else
    echo "Wheel NOPASS already configured, please verify"
  fi
}

configAdminSudo() {
  if [[ "$checkDevopsSudoer" == "" ]] || [[ "$checkDevopsSudoer" == "#" ]]; then
    sed -i '/wheel.*NOPASSWD/c\%admin  ALL=(ALL)       NOPASSWD: ALL' /etc/sudoers
  else
    echo "admin NOPASS already configured, please verify"
  fi
}

if [[ "$group" == "wheel" ]]; then
  configWheelSudo
elif [[ "$group" == "devops" ]]; then
  configAdminSudo
fi
