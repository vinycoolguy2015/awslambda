#!/bin/sh
ldapsearch -x \
  '(&(objectClass=ldapPublicKey)(uid='"$1"'))' \
  'sshPublicKey' \
  | sed -n '/^ /{H;d};/sshPublicKey:/x;$g;s/\n *//g;s/sshPublicKey: //gp'
