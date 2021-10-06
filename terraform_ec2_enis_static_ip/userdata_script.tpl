if [ "$(uname -r|grep 'el'|grep 'x86_64')x" != "x" ]; then

#Identify the second network Interface

#NET2=`nmcli device status |grep disconnected|awk '{print $1}'`
NET2=`nmcli device|grep ethernet|awk 'FNR == 2 {print $1}'`

logger -p local0.info "Second Netowrk Device is $NET2. Will try to configure it."

  # Create ifcfg-$NET2 for second network_interface
  #Interface file for $NET2
  echo BOOTPROTO=dhcp >> /etc/sysconfig/network-scripts/ifcfg-$NET2
  echo DEVICE=$NET2  >> /etc/sysconfig/network-scripts/ifcfg-$NET2
  echo ONBOOT=yes  >> /etc/sysconfig/network-scripts/ifcfg-$NET2
  echo TYPE=Ethernet  >> /etc/sysconfig/network-scripts/ifcfg-$NET2
  echo USERCTL=no  >> /etc/sysconfig/network-scripts/ifcfg-$NET2

  #bring up the Interface
  ifup $NET2

  #Capture IP details
  IP=`ifconfig $NET2|grep "inet "|awk '{print $2}'`
        until [[ $IP =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; do
    sleep 5 && let cntr=cntr+1
    IP=`ifconfig $NET2|grep "inet "|awk '{print $2}'`
  done

  MASK=`ifconfig $NET2|grep "inet "|awk '{print $4}'`
  SUBNET=`ipcalc -n $IP $MASK|awk -F'=' '{print $2}'`
  PREFIX=`ipcalc -p $IP $MASK|awk -F'=' '{print $2}'`
  MAC=`ifconfig $NET2|grep ether|awk '{print $2}'`

  #Calculate default route for $NET2
  X=`echo $SUBNET|awk -F'.' '{print $4}'`
  OCT4=$(( X + 1 ))
  DEFROUTE=`echo $SUBNET |awk -F '.' '{print $1"."$2"."$3}'`.$OCT4

  #Create Static config file for $NET2
  mv /etc/sysconfig/network-scripts/ifcfg-$NET2 /etc/sysconfig/network-scripts/ifcfg-$NET2.`date +%Y%m%d%H%M%S`
  echo BOOTPROTO=none > /etc/sysconfig/network-scripts/ifcfg-$NET2
  echo DEVICE=$NET2  >> /etc/sysconfig/network-scripts/ifcfg-$NET2
  echo IPADDR=$IP >> /etc/sysconfig/network-scripts/ifcfg-$NET2
  echo NETMASK=$MASK >> /etc/sysconfig/network-scripts/ifcfg-$NET2
  echo HWADDR=$MAC >> /etc/sysconfig/network-scripts/ifcfg-$NET2
  echo ONBOOT=yes  >> /etc/sysconfig/network-scripts/ifcfg-$NET2
  echo TYPE=Ethernet  >> /etc/sysconfig/network-scripts/ifcfg-$NET2
  echo USERCTL=no  >> /etc/sysconfig/network-scripts/ifcfg-$NET2
  #echo NM_CONTROLLED=no >> /etc/sysconfig/network-scripts/ifcfg-$NET2

  #Create route table for $NET2
  cp -p /etc/iproute2/rt_tables /etc/iproute2/rt_tables.`date +%Y%m%d%H%M%S`
  echo "999 mgmt" >> /etc/iproute2/rt_tables

  #Create routes for $NET2
  echo "$SUBNET/$PREFIX dev $NET2 table mgmt" > /etc/sysconfig/network-scripts/route-$NET2
  echo "default via $DEFROUTE dev $NET2 table mgmt" >> /etc/sysconfig/network-scripts/route-$NET2

  #Create route rule_action
  echo "from $IP/32 lookup mgmt" > /etc/sysconfig/network-scripts/rule-$NET2

  #restart $NET2
  ifdown $NET2
  ifup $NET2
fi
