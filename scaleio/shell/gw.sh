#!/bin/bash


exec 1>> /tmp/deploy_ming/log/gw.log 2>> /tmp/deploy_ming/log/gw.log

/usr/bin/touch 123

IPADDRESS=$( grep jumpbox ../config/ip_val | awk -F ":" '{print $2}')

MDMADDRESS=$( grep mdm_ip ../config/ip_val | awk -F ":" '{print $2}')

/usr/bin/scp -o StrictHostKeyChecking=no -i ../config/id_rsa root@$IPADDRESS:/tmp/software/jre-8u121-linux-x64.rpm /tmp/deploy_ming/software/

/usr/bin/scp -o StrictHostKeyChecking=no -i ../config/id_rsa root@$IPADDRESS:/tmp/software/EMC-ScaleIO-gateway-2.0-13000.211.x86_64.rpm /tmp/deploy_ming/software/

/usr/bin/scp -o StrictHostKeyChecking=no -i ../config/id_rsa root@$IPADDRESS:/tmp/software/EMC-ScaleIO-gateway-2.0-14009.107.x86_64.rpm /tmp/deploy_ming/software/


/bin/sudo /bin/su - root  <<EOF


/bin/rpm -U /tmp/deploy_ming/software/jre-8u121-linux-x64.rpm

GATEWAY_ADMIN_PASSWORD="9HE2hw"   /bin/rpm -U /tmp/deploy_ming/software/EMC-ScaleIO-gateway-2.0-13000.211.x86_64.rpm

#scale-gateway

/usr/bin/sed -i.$(date +%Y%M%d) 's/mdm.ip.addresses=/&$MDMADDRESS/' /opt/emc/scaleio/gateway/webapps/ROOT/WEB-INF/classes/gatewayUser.properties 

#UIM地址

#cat /opt/emc/scaleio/gateway/conf/server.xml

sed -i.$(date +%Y%M%d) 's/sslEnabledProtocols="TLSv1.2,TLSv1.1,TLSv1"/sslEnabledProtocols="TLSv1.2"/g'  /opt/emc/scaleio/gateway/conf/server.xml

EOF