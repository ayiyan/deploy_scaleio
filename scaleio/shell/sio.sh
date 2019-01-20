#!/bin/bash

exec 1>> /tmp/deploy_ming/log/sio.log 2>> /tmp/deploy_ming/log/sio.log

/usr/bin/touch 123

IPADDRESS=$( grep jumpbox ../config/ip_val | awk -F ":" '{print $2}')

/usr/bin/scp -o StrictHostKeyChecking=no -i ../config/id_rsa root@$IPADDRESS:/tmp/software/perccli_7.1-007.0127_linux.tar.gz /tmp/deploy_ming/software/



/bin/sudo /bin/su - root  <<EOF

/bin/tar -zxvf  /tmp/deploy_ming/software/perccli_7.1-007.0127_linux.tar.gz -C /tmp/deploy_ming/software/

/bin/rpm -ivh /tmp/deploy_ming/software/Linux/perccli-007.0127.0000.0000-1.noarch.rpm



#rsyslog[虚拟机已测]
/usr/bin/sed -i.$(date +%Y%M%d) '/Provides TCP syslog reception/{:c;N;s/#$Input/$Input/;s/#$ModLoad/$ModLoad/;bc}' /etc/rsyslog.conf 
/usr/bin/sed -i '/^\$ModLoad imtcp/a\\input(type="imtcp" address="127.0.0.1")' /etc/rsyslog.conf
/usr/bin/sed -i '/@@remote-host/a\\# Local MDM syslog' /etc/rsyslog.conf
/usr/bin/sed -i '/^\# Local MDM syslog/a\\local0.*                /var/log/mdm-syslog.log' /etc/rsyslog.conf
/usr/bin/sed -i.$(date +%Y%M%d) '/spooler/a\\/var/log/mdm-syslog.log' /etc/logrotate.d/syslog
/usr/bin/systemctl restart rsyslog
EOF