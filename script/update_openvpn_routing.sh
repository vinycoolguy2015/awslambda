#!/bin/bash
  
FILE=/home/openvpnas/dont_delete_ip.txt #Store current IP address in this file
dig +short test.com | tail -n2 >/tmp/current_ip.txt

if test -f "$FILE"; then
    previous_ip_address=`cat $FILE`
    current_ip_address=`cat /tmp/current_ip.txt`
    if [ ! -z "$previous_ip_address" ] && [ ! -z "$current_ip_address" ];then
        diff $FILE /tmp/current_ip.txt
        if [ "$?" == 0 ];then
            echo "IP Not Changed"
        else
            for ip in $previous_ip_address
                do
                    rule_number=`/usr/local/openvpn_as/scripts/sacli ConfigQuery | grep $ip/32 | cut -d "\"" -f2 | cut -d "." -f5`
                    /usr/local/openvpn_as/scripts/sacli --key "vpn.server.routing.private_network.$rule_number" --value "$ip/32" ConfigDel
                done
            for ip in $current_ip_address
                do
                    current_rule_count=`/usr/local/openvpn_as/scripts/sacli ConfigQuery | grep vpn.server.routing.private_network | wc -l`
                    /usr/local/openvpn_as/scripts/sacli --key "vpn.server.routing.private_network.$current_rule_count" --value "$ip/32" ConfigPut
                done
            /usr/local/openvpn_as/scripts/sacli start
            cp /tmp/current_ip.txt $FILE
        fi
    fi
fi
