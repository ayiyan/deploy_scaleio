#!/bin/bash

exec 1>> /tmp/deploy_ming/log/httpd.log 2>> /tmp/deploy_ming/log/httpd.log

/usr/bin/touch 123

IPADDRESS=$( grep jumpbox ../config/ip_val | awk -F ":" '{print $2}')

/usr/bin/scp -o StrictHostKeyChecking=no -i ../config/id_rsa root@$IPADDRESS:/tmp/software/tomcat-connectors-1.2.42-src.tar.gz /tmp/deploy_ming/software/

yum install -y  httpd-devel apr apr-devel apr-util apr-util-devel gcc gcc-c++ make autoconf libtool mod_ssl keepalived

/usr/bin/mkdir -p /opt/mod_jk

/usr/bin/tar -zxvf  /tmp/deploy_ming/software/tomcat-connectors-1.2.42-src.tar.gz -C /opt/mod_jk/


cd /opt/mod_jk/tomcat-connectors-1.2.42-src/native/

touch 456

/opt/mod_jk/tomcat-connectors-1.2.42-src/native/configure --with-apxs=/usr/bin/apxs
/usr/bin/make 
/usr/bin/libtool --finish /usr/lib64/httpd/modules 
/usr/bin/make install


sudo /usr/bin/cp  /tmp/deploy_ming/template/mod_jk.conf /etc/httpd/conf.d/ 

sudo /usr/bin/cp /tmp/deploy_ming/template/workers.properties /etc/httpd/conf.d/


GW1_NAME_VAL=$(grep gw1 /tmp/deploy_ming/config/hostlist |  awk -F ":"  '{print $2}')
GW1_IP_VAL=$(grep gw1 /tmp/deploy_ming/config/hostlist    | awk -F ":"  '{print $3}')
GW2_NAME_VAL=$(grep gw2  /tmp/deploy_ming/config/hostlist   | awk -F ":"  '{print $2}')
GW2_IP_VAL=$(grep gw2  /tmp/deploy_ming/config/hostlist   | awk -F ":"  '{print $3}')


sudo /usr/bin/sed -i  s/{GW1-NAME}/$GW1_NAME_VAL/g   /etc/httpd/conf.d/workers.properties

sudo /usr/bin/sed -i -e "s/{GW1-NAME}/$GW1_NAME_VAL/g" -e "s/{GW2-NAME}/$GW2_NAME_VAL/g"  /etc/httpd/conf.d/workers.properties
sudo /usr/bin/sed -i -e "s/{GW1-IP}/$GW1_IP_VAL/g" -e "s/{GW2-IP}/$GW2_IP_VAL/g"  /etc/httpd/conf.d/workers.properties

HTTPD_VIP_VAL=$(grep httpd_vip /tmp/deploy_ming/config/ip_val | awk -F":" '{print $2}')

sudo /usr/bin/sed -i.$(date +%Y%M%d)  "s/_default_/$HTTPD_VIP_VAL/g" /etc/httpd/conf.d/ssl.conf

sudo /usr/bin/sed -i -e 's/^SSLCertificateFile/#SSLCertificateFile/g' -e 's/^SSLCertificateKeyFile/#SSLCertificateKeyFile/g' /etc/httpd/conf.d/ssl.conf

sudo /usr/bin/sed -i '/^<VirtualHost/a\\JkMount /* balance1'  /etc/httpd/conf.d/ssl.conf 
sudo /usr/bin/sed -i '/^<VirtualHost/a\\JkMountCopy On'  /etc/httpd/conf.d/ssl.conf  
sudo /usr/bin/sed -i '/^<VirtualHost/a\\SSLCertificateFile SSLCertificateKeyFile /etc/httpd/certs/filename-key.pem'  /etc/httpd/conf.d/ssl.conf
sudo /usr/bin/sed -i '/^<VirtualHost/a\\SSLCertificateFile /etc/httpd/certs/filename-cert.pem'  /etc/httpd/conf.d/ssl.conf 


sudo sed -i   '/^<Directory \"\/var\/www\">/{:c;N;s/AllowOverride None/AllowOverride All/;bc}'    /etc/httpd/conf/httpd.conf

sudo /usr/bin/sed -i "/ServerName www.example.com/a\\ServerName $HTTPD_VIP_VAL"  /etc/httpd/conf/httpd.conf

sudo /usr/bin/cp /tmp/deploy_ming/template/keepalived.conf   /etc/keepalived/keepalived.conf

GW1_HOST=$(grep httpd1 /tmp/deploy_ming/config/hostlist | awk -F ":" '{print $2}')
GW2_HOST=$(grep httpd2 /tmp/deploy_ming/config/hostlist | awk -F ":" '{print $2}')

HTTPD_VIP=$(grep httpd_vip /tmp/deploy_ming/config/ip_val | awk -F ":" '{print $2}')

sudo mkdir -p /etc/httpd/certs


if [ $GW1_HOST == $(hostname) ]; then
   sudo /usr/bin/sed -i s/{priority}/101/g  /etc/keepalived/keepalived.conf
   sudo /usr/bin/sed -i s/{httpd-vip}/$HTTPD_VIP/g  /etc/keepalived/keepalived.conf
   cd /etc/httpd/certs/
   sudo /usr/bin/openssl  req -newkey rsa:2048 -nodes  -keyout key.pem -x509 -days 365 -out certficate.pem -subj /C=ES/L=Milenium/O=Telefonica/OU=UNICA/CN=10.42.116.247	 
   sudo /usr/bin/openssl  x509 -text -noout -in certficate.pem 
   sudo /usr/bin/openssl  pkcs12 -inkey key.pem  -in certficate.pem -passout pass:Ming2613  -export  -out certficate.p12
   sudo /usr/bin/openssl  pkcs12 -in certficate.p12 -passin pass:12345   -noout -info
   sudo /usr/bin/openssl  pkcs12 -in certficate.p12  -nocerts -passin pass:Ming2613  -nodes -out filename-key.pem
   sudo /usr/bin/openssl  pkcs12 -in certficate.p12  -clcerts -nokeys -passin pass:Ming2613 -out  filename-cert.pem
   sudo /usr/bin/scp -o StrictHostKeyChecking=no -i /tmp/deploy_ming/config/id_rsa  /etc/httpd/certs/filename-key.pem  root@$IPADDRESS:/tmp/
   sudo /usr/bin/scp -o StrictHostKeyChecking=no -i /tmp/deploy_ming/config/id_rsa  /etc/httpd/certs/filename-cert.pem  root@$IPADDRESS:/tmp/
elif  [ $GW2_HOST == $(hostname) ]; then
   sudo /usr/bin/sed -i s/{priority}/100/g  /etc/keepalived/keepalived.conf
   sudo /usr/bin/sed -i s/{httpd-vip}/$HTTPD_VIP/g  /etc/keepalived/keepalived.conf
   while true
   do
      STATE_NUM=$(ssh -i /tmp/deploy_ming/config/id_rsa root@192.168.1.108 "ls /tmp/ |  grep -E  'filename-cert.pem|filename-key.pem'")
      echo $STATE_NUM
      if [[ $STATE_NUM  =~ "filename-cert.pem" &&  $STATE_NUM =~ "filename-key.pem" ]]; 
      	then
        	sudo /usr/bin/scp -o StrictHostKeyChecking=no -i /tmp/deploy_ming/config/id_rsa  root@$IPADDRESS:/tmp/filename-key.pem  /etc/httpd/certs/  
        	sudo /usr/bin/scp -o StrictHostKeyChecking=no -i /tmp/deploy_ming/config/id_rsa  root@$IPADDRESS:/tmp/filename-cert.pem /etc/httpd/certs/        
   			sleep 3
   			break
      fi         
   done

else
	echo ""
fi

/bin/sudo /bin/su - root  <<EOF

echo "net.ipv4.ip_nonlocal_bind = 1" >> /etc/sysctl.conf 

EOF

sudo /usr/sbin/sysctl -p

sudo /usr/bin/systemctl stop keepallived.service
sudo /usr/bin/systemctl start keepalived.service
sudo /usr/bin/systemctl enable keepalived.service

sudo /usr/bin/sed -i.$(date +%Y%M%d) 's/SSLProtocol all -SSLv2 -SSLv3/SSLProtocol -all +TLSv1.2/g'  /etc/httpd/conf.d/ssl.conf 

