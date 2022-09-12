#!/bin/bash
  
RESET_USER=$1
echo $RESET_USER
if [[  -z $RESET_USER  ]]; then
  echo What is the userid you want to reset the id?
  read RESET_USER
fi

echo Resetting $RESET_USER
echo Executing sudo /usr/local/openvpn_as/scripts/sacli --user $RESET_USER --lock 0 GoogleAuthRegen
sudo /usr/local/openvpn_as/scripts/sacli --user $RESET_USER --lock 0 GoogleAuthRegen

retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Error resetting $RESET_USER MFA"
else
    echo "Successful reset $RESET_USER MFA"
fi
exit $retVal
