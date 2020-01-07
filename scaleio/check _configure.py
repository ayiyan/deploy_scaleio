#!/usr/bin/env python
#coding=utf-8

import os
import re
import time
import threading
from paramiko import SSHClient, AutoAddPolicy, SFTPClient, Transport

def CONNECTION(Func):
    def inner(Mem,HOST_DICT,HOST_KEYS_VAL):
        COUNTER=0
        for GW_LIST in HOST_DICT[HOST_KEYS_VAL]:
            COUNTER +=1
            IPADDRESS = GW_LIST[0]
            PORT = GW_LIST[1]
            USERNAME = GW_LIST[2]
            PASSWORD = GW_LIST[3]
            CLIENT = SSHClient()
            CLIENT.set_missing_host_key_policy(AutoAddPolicy())
            CLIENT.connect(IPADDRESS, port=PORT, username=USERNAME, password=PASSWORD)
            Func(COUNTER, HOST_KEYS_VAL, CLIENT)
    return inner


class HOST:
    def __init__(self):
        self.RUN()       

    # HTTP Node Software Check
    @CONNECTION
    def HTTPD(COUNTER,HOST_KEYS_VAL, CLIENT):
        Software_List= [
                        'httpd-devel',
                        'apr',
                        'apr-devel',
                        'apr-util',
                        'apr-util-devel',
                        'gcc',
                        'gcc-c++',
                        'make',
                        'autoconf',
                        'libtool'
                        ]
        Service_List = [
                        'keepalived.service',
                        'httpd.service'
                        ]
        for Software_List_Val in Software_List:
            #stdin, stdout, stderr = CLIENT.exec_command('rpm -qa | grep Software_List_Val ')
            stdin, stdout, stderr = CLIENT.exec_command('rpm -qa | grep %s > /dev/null  && echo 0 || echo 1'%(Software_List_Val))
            Software_Val_Num = (bytes.decode(stdout.read())).strip()
            if int(Software_Val_Num) == 0:
                print("%s %s Software is: ---> \033[32m[OK]\033[0m"%(HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"), Software_List_Val))
            else:
                print("%s %s Software is: ---> \033[31m[Failed]\033[0m"%(HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"), Software_List_Val))

        for Service_List_Val in Service_List:
            stdin, stdout, stderr = CLIENT.exec_command("systemctl list-unit-files  | grep %s |awk '{print $2}'"%(Service_List_Val) )
            if (bytes.decode(stdout.read())).strip("\n") == "enabled":
                print("%s %s  Auto-Start  is: ---> \033[32m[OK]\033[0m" % (HOST_KEYS_VAL.replace("]", str(COUNTER) + "]"), Service_List_Val))
            else:
                print("%s %s  Auto-Start is: ---> \033[31m[Failed]\033[0m" % (HOST_KEYS_VAL.replace("]", str(COUNTER) + "]"), Service_List_Val))

            stdin, stdout, stderr = CLIENT.exec_command("systemctl is-active %s"%(Service_List_Val) )
            if (bytes.decode(stdout.read())).strip("\n") == "active":
                print("%s %s  Status is: ---> \033[32m[OK]\033[0m" % (HOST_KEYS_VAL.replace("]", str(COUNTER) + "]"), Service_List_Val))
            else:
                print("%s %s  Status is: ---> \033[31m[Failed]\033[0m" % (HOST_KEYS_VAL.replace("]", str(COUNTER) + "]"), Service_List_Val))





    # NFS Node Software Check
    @CONNECTION
    def NFS(COUNTER,HOST_KEYS_VAL, CLIENT):

        Software_List= [
                        'pcs',
                        'pacemaker',
                        'fence-agents-all',
                        'fence-virt',
                        'nfs-utils',
                        'libnfsidmap'
                        ]

        Service_List = [
                        'pcsd.service'
        ]

        for Software_List_Val in Software_List:
            stdin, stdout, stderr = CLIENT.exec_command('rpm -qa | grep %s > /dev/null  && echo 0 || echo 1'%(Software_List_Val))
            Software_Val_Num = (bytes.decode(stdout.read())).strip()
            if int(Software_Val_Num) == 0:
                print("%s %s Software is: ---> \033[32m[OK]\033[0m"%(HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"), Software_List_Val))
            else:
                print("%s %s Software is: ---> \033[31m[Failed]\033[0m"%(HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"), Software_List_Val))

        for Service_List_Val in Service_List:
            stdin, stdout, stderr = CLIENT.exec_command("systemctl list-unit-files  | grep %s |awk '{print $2}'"%(Service_List_Val) )
            if (bytes.decode(stdout.read())).strip("\n") == "enabled":
                print("%s %s  Auto-Start  is: ---> \033[32m[OK]\033[0m" % (HOST_KEYS_VAL.replace("]", str(COUNTER) + "]"), Service_List_Val))
            else:
                print("%s %s  Auto-Start is: ---> \033[31m[Failed]\033[0m" % (HOST_KEYS_VAL.replace("]", str(COUNTER) + "]"), Service_List_Val))

            stdin, stdout, stderr = CLIENT.exec_command("systemctl is-active %s"%(Service_List_Val) )
            if (bytes.decode(stdout.read())).strip("\n") == "active":
                print("%s %s   Status is: ---> \033[32m[OK]\033[0m" % (HOST_KEYS_VAL.replace("]", str(COUNTER) + "]"), Service_List_Val))
            else:
                print("%s %s   Status is: ---> \033[31m[Failed]\033[0m" % (HOST_KEYS_VAL.replace("]", str(COUNTER) + "]"), Service_List_Val))

      


    # GW Node Software Check
    @CONNECTION
    def GW(COUNTER,HOST_KEYS_VAL, CLIENT):
        Service_List = [
                        'scaleio-gateway.service'
                        ]

        for Service_List_Val in Service_List:
            stdin, stdout, stderr = CLIENT.exec_command("systemctl list-unit-files  | grep %s |awk '{print $2}'"%(Service_List_Val))
            if (bytes.decode(stdout.read())).strip('\n') == "enabled":
                print("%s %s  Auto-Start  is: ---> \033[32m[OK]\033[0m" % (HOST_KEYS_VAL.replace("]", str(COUNTER) + "]"), Service_List_Val))
            else:
                print("%s %s  Auto-Start is: ---> \033[31m[Failed]\033[0m" % (HOST_KEYS_VAL.replace("]", str(COUNTER) + "]"), Service_List_Val))

            stdin, stdout, stderr = CLIENT.exec_command("systemctl is-active %s"%(Service_List_Val) )
            if (bytes.decode(stdout.read())).strip('\n') == "active":
                print("%s %s   Status  is: ---> \033[32m[OK]\033[0m" % (HOST_KEYS_VAL.replace("]", str(COUNTER) + "]"), Service_List_Val))
            else:
                print("%s %s   Status  is: ---> \033[31m[Failed]\033[0m" % (HOST_KEYS_VAL.replace("]", str(COUNTER) + "]"), Service_List_Val))
                      
        stdin, stdout, stderr = CLIENT.exec_command("sudo  cat /opt/emc/scaleio/gateway/conf/server.xml | grep Connector | grep 8443 > /dev/null && echo 0 || echo 1")
        if int((bytes.decode(stdout.read())).strip('\n')) == 0:
            print("%s  server.xmlConfigure File  is: ---> \033[32m[OK]\033[0m" % (HOST_KEYS_VAL.replace("]", str(COUNTER)) + "]"))
        else:
            print("%s  server.xml Configure File  is: ---> \033[31m[Failed]\033[0m" % (HOST_KEYS_VAL.replace("]", str(COUNTER)) + "]"))

        stdin, stdout, stderr = CLIENT.exec_command("sudo cat /opt/emc/scaleio/gateway/conf/server.xml| grep $(hostname) >/dev/null &&echo 0 || echo 1")
        if int((bytes.decode(stdout.read())).strip('\n')) == 0:
            print("%s  server.xmlConfigure File  is: ---> \033[32m[OK]\033[0m" % (HOST_KEYS_VAL.replace("]", str(COUNTER)) + "]"))
        else:
            print("%s  server.xml Configure File  is: ---> \033[31m[Failed]\033[0m" % (HOST_KEYS_VAL.replace("]", str(COUNTER)) + "]"))

        stdin, stdout, stderr = CLIENT.exec_command("sudo  cat  /opt/emc/scaleio/gateway/conf/server.xml  | grep sslEnabledProtocols |awk -F '=' '{print $2}'")
        if (bytes.decode(stdout.read())).strip('\n') == '"TLSv1.2"':
            print("%s  server.xml Configure File SSL is: ---> \033[32m[OK]\033[0m" % (HOST_KEYS_VAL.replace("]", str(COUNTER)) + "]"))
        else:
            print("%s  server.xml Configure File SSL is: ---> \033[31m[Failed]\033[0m" % (HOST_KEYS_VAL.replace("]", str(COUNTER)) + "]"))

        stdin, stdout, stderr = CLIENT.exec_command("sudo  cat /opt/emc/scaleio/gateway/webapps/ROOT/WEB-INF/classes/gatewayUser.properties | grep 'features.enable_snmp' |awk -F '=' '{print $2}'")
        if (bytes.decode(stdout.read())).strip('\n') == 'true':
            print("%s  server.xml Configure File SNMP is: ---> \033[32m[OK]\033[0m" % (HOST_KEYS_VAL.replace("]", str(COUNTER)) + "]"))
        else:
            print("%s  server.xml Configure File SNMP is: ---> \033[31m[Failed]\033[0m" % (HOST_KEYS_VAL.replace("]", str(COUNTER)) + "]"))

        stdin, stdout, stderr = CLIENT.exec_command(" sudo  cat /opt/emc/scaleio/gateway/webapps/ROOT/WEB-INF/classes/gatewayUser.properties | grep 'snmp.traps_receiver_ip' |grep -o  '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' >/dev/null &&echo 0 || echo 1")
        if int((bytes.decode(stdout.read())).strip('\n')) == 0:
            print("%s  server.xml Configure File UIM IP is: ---> \033[32m[OK]\033[0m" % (HOST_KEYS_VAL.replace("]", str(COUNTER)) + "]"))
        else:
            print("%s  server.xml Configure File UIM IP is: ---> \033[31m[Failed]\033[0m" % (HOST_KEYS_VAL.replace("]", str(COUNTER)) + "]"))



    # SIO Node Software Check
    @CONNECTION
    def SIO(COUNTER,HOST_KEYS_VAL, CLIENT):
        Software_List= [
                        'ntp',
                        'fence-virtd',
                        'fence-virtd-multicast',
                        'fence-virtd-libvirt',
                        'fence-virt*',
                        'perccl'
                        ]
        Service_List = [
                        'rsyslog.service'
                        ]             
        for Software_List_Val in Software_List:
            stdin, stdout, stderr = CLIENT.exec_command('rpm -qa | grep %s > /dev/null  && echo 0 || echo 1'%(Software_List_Val))
            Software_Val_Num = (bytes.decode(stdout.read())).strip()
            if int(Software_Val_Num) == 0:
                print("%s %s Software is: ---> \033[32m[OK]\033[0m"%(HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"), Software_List_Val))
            else:
                print("%s %s Software is: ---> \033[31m[Failed]\033[0m"%(HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"), Software_List_Val))

        for Service_List_Val in Service_List:
            stdin, stdout, stderr = CLIENT.exec_command("systemctl list-unit-files  | grep %s |awk '{print $2}'"%(Service_List_Val) )
            if (bytes.decode(stdout.read())).strip('\n') == "enabled":
                print("%s %s  Auto-Start  is: ---> \033[32m[OK]\033[0m" % (HOST_KEYS_VAL.replace("]", str(COUNTER) + "]"), Service_List_Val))
            else:
                print("%s %s  Auto-Start is: ---> \033[31m[Failed]\033[0m" % (HOST_KEYS_VAL.replace("]", str(COUNTER) + "]"), Service_List_Val))

            stdin, stdout, stderr = CLIENT.exec_command("systemctl is-active %s"%(Service_List_Val) )
            if (bytes.decode(stdout.read())).strip('\n') == "active":
                print("%s %s   Status  is: ---> \033[32m[OK]\033[0m" % (HOST_KEYS_VAL.replace("]", str(COUNTER) + "]"), Service_List_Val))
            else:
                print("%s %s   Status  is: ---> \033[31m[Failed]\033[0m" % (HOST_KEYS_VAL.replace("]", str(COUNTER) + "]"), Service_List_Val))


        if (HOST_KEYS_VAL.replace("]", str(COUNTER)) + "]") == "[sio1]" or (HOST_KEYS_VAL.replace("]", str(COUNTER)) + "]") == "[sio2]":

            stdin, stdout, stderr = CLIENT.exec_command("cat /etc/rsyslog.conf | grep '^\$ModLoad imtcp' > /dev/null  && echo 0 || echo 1")
            if int((bytes.decode(stdout.read())).strip('\n')) == 0:
                print("%s  Rsyslog Configure File  is: ---> \033[32m[OK]\033[0m" % (HOST_KEYS_VAL.replace("]", str(COUNTER)) + "]"))
            else:
                print("%s  Rsyslog Configure File  is: ---> \033[31m[Failed]\033[0m" % (HOST_KEYS_VAL.replace("]", str(COUNTER)) + "]"))

            stdin, stdout, stderr = CLIENT.exec_command("cat /etc/rsyslog.conf | grep 'input'  > /dev/null  && echo 0 || echo 1")
            if int((bytes.decode(stdout.read())).strip('\n')) == 0:
                print("%s  Rsyslog Configure File  is: ---> \033[32m[OK]\033[0m" % (HOST_KEYS_VAL.replace("]", str(COUNTER)) + "]"))
            else:
                print("%s  Rsyslog Configure File  is: ---> \033[31m[Failed]\033[0m" % (HOST_KEYS_VAL.replace("]", str(COUNTER))+ "]"))
                                
            stdin, stdout, stderr = CLIENT.exec_command("cat /etc/rsyslog.conf | grep 'InputTCPServerRun' > /dev/null  && echo 0 || echo 1")
            if int((bytes.decode(stdout.read())).strip('\n')) == 0:
                print("%s  Rsyslog Configure File  is: ---> \033[32m[OK]\033[0m" % (HOST_KEYS_VAL.replace("]", str(COUNTER)) + "]"))
            else:
                print("%s  Rsyslog Configure File  is: ---> \033[31m[Failed]\033[0m" % (HOST_KEYS_VAL.replace("]", str(COUNTER))+ "]"))
                                
            stdin, stdout, stderr = CLIENT.exec_command("cat /etc/rsyslog.conf | grep  'local0.*' > /dev/null  && echo 0 || echo 1")
            if int((bytes.decode(stdout.read())).strip('\n')) == 0:
                print("%s  Rsyslog Configure File  is: ---> \033[32m[OK]\033[0m" % (HOST_KEYS_VAL.replace("]", str(COUNTER)) + "]"))
            else:
                print("%s  Rsyslog Configure File  is: ---> \033[31m[Failed]\033[0m" % (HOST_KEYS_VAL.replace("]", str(COUNTER)) + "]"))
                                
    
    @CONNECTION
    def PUBLIC(COUNTER,HOST_KEYS_VAL, CLIENT):

        
        # Check Get Hostname
        stdin, stdout, stderr = CLIENT.exec_command('hostname')
        HOSTNAME_VAL = (bytes.decode(stdout.read())).strip()
        #print("%s %s "%(HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"), HOSTNAME_VAL))

        stdin, stdout, stderr = CLIENT.exec_command("cat /etc/resolv.conf  | grep search  | awk '{print $2}'")
        DOMAIN_VAL= (bytes.decode(stdout.read()))


        #Check PING TEST DNS&ECAS
        stdin, stdout, stderr = CLIENT.exec_command('/usr/sbin/ip addr | grep -v mdm | grep -o -P "(\d+\.)(\d+\.)(\d+\.)(\d+)/25" |grep -v -E "127.|192."')
        IPADDRESS_VAL= (bytes.decode(stdout.read()).replace('/25','').strip('\n'))
        print(IPADDRESS_VAL, HOSTNAME_VAL+"."+DOMAIN_VAL.strip('\n'), HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"))
        #print(IPADDRESS_VAL, HOSTNAME_VAL)

        '''
        
        #Check PING TEST DNS&ECAS
        stdin, stdout, stderr = CLIENT.exec_command('ping -c 1 192.168.87.248 > /dev/null   && echo 0 || echo 1')
        PING_VAL1 = bytes.decode(stdout.read())
        if int(PING_VAL1) == 0:
            print("%s %s Ping 192.168.87.248 is: ---> \033[32m[OK]\033[0m"%(HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"), IPADDRESS_VAL))
        else:
            print("%s %s Ping 192.168.87.248 is: ---> \033[31m[Failed]\033[0m"%(HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"), IPADDRESS_VAL))
      

        #Check PING TEST DNS&ECAS      
        stdin, stdout, stderr = CLIENT.exec_command('ping -c 1 192.168.187.248 > /dev/null   && echo 0 || echo 1')
        PING_VAL2 = bytes.decode(stdout.read())
        if int(PING_VAL2) == 0:
            print("%s %s Ping 192.168.187.248 is: ---> \033[32m[OK]\033[0m"%(HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"), IPADDRESS_VAL))
        else:
            print("%s %s Ping 192.168.187.248 is: ---> \033[31m[Failed]\033[0m"%(HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"), IPADDRESS_VAL))

        #Check PING TEST DNS&ECAS
        stdin, stdout, stderr = CLIENT.exec_command('ping -c 1 192.168.115.20 > /dev/null   && echo 0 || echo 1')
        PING_VAL3 = bytes.decode(stdout.read())
        if int(PING_VAL3) == 0:
            print("%s %s Ping 192.168.115.20 is: ---> \033[32m[OK]\033[0m"%(HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"), IPADDRESS_VAL))
        else:
            print("%s %s Ping 192.168.115.20 is: ---> \033[31m[Failed]\033[0m"%(HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"), IPADDRESS_VAL))

        

        #Check PING TEST DNS&ECAS
        stdin, stdout, stderr = CLIENT.exec_command('ping -c 1 192.168.15.20 > /dev/null   && echo 0 || echo 1')
        PING_VAL3 = bytes.decode(stdout.read())
        if int(PING_VAL3) == 0:
            print("%s %s Ping 192.168.15.20 is: ---> \033[32m[OK]\033[0m"%(HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"), IPADDRESS_VAL))
        else:
            print("%s %s Ping 192.168.15.20 is: ---> \033[31m[Failed]\033[0m"%(HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"), IPADDRESS_VAL))

       
        
        # Modify  PermitRoot no--->yes
        stdin, stdout, stderr = CLIENT.exec_command('sudo sed -i.bak  "s/^PermitRootLogin no/PermitRootLogin yes/g" /etc/ssh/sshd_config')
        FIREWALL_VAL= bytes.decode(stdout.read())
        stdin, stdout, stderr = CLIENT.exec_command('sudo systemctl restart sshd')

        # # Modify  PermitRoot yes--->no
        # stdin, stdout, stderr = CLIENT.exec_command('sudo sed -i.bak  "s/^PermitRootLogin yes/PermitRootLogin no/g" /etc/ssh/sshd_config')
        # FIREWALL_VAL= bytes.decode(stdout.read())
        # stdin, stdout, stderr = CLIENT.exec_command('sudo systemctl restart sshd')


        # /etc/resoly.conf
        # stdin, stdout, stderr = CLIENT.exec_command('sudo cat /etc/resolv.conf | grep search')
        # DOMAIN_VAL = bytes.decode(stdout.read())
        # print(HOSTNAME_VAL,"--->",DOMAIN_VAL)


        # Check iptables
        stdin, stdout, stderr = CLIENT.exec_command('sudo systemctl stop iptables')
        stdin, stdout, stderr = CLIENT.exec_command('sudo systemctl is-active iptables')
        FIREWALL_VAL= (bytes.decode(stdout.read())).strip('\n')
        if FIREWALL_VAL.strip() == "active":
            print("%s %sFireWall ---> \033[32m[Open]\033[0m"%(HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"), HOSTNAME_VAL))
        else:
            print("%s %s FireWall ---> \033[31m[Close]\033[0m"%(HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"), HOSTNAME_VAL))
        
        
        

        # Check RootLogin
        stdin, stdout, stderr = CLIENT.exec_command("sudo grep -i ^PermitRootLogin /etc/ssh/sshd_config | awk '{print $2}'")
        ROOTLOGIN_VAL= bytes.decode(stdout.read())
        if ROOTLOGIN_VAL.strip() == "no":
            print("%s %s PermitRootLogin ---> \033[32m[Closed]\033[0m"%(HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"), HOSTNAME_VAL))
        else:
            print("%s %s PermitRootLogin ---> \033[31m[Active]\033[0m"%(HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"), HOSTNAME_VAL))


        # Check Port:80
        stdin, stdout, stderr = CLIENT.exec_command("sudo lsof -i :80")
        HTTPPORT_VAL= bytes.decode(stdout.read())
        if HTTPPORT_VAL.strip() == "":
            print("%s %s HTTPPORT ---> \033[32m[Closed]\033[0m"%(HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"), HOSTNAME_VAL))
        else:
            print("%s %s HTTPPORT ---> \033[31m[Active]\033[0m"%(HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"), HOSTNAME_VAL))
        
        '''    


    def RUN(self):
        INVENTORY = open('config\inventory')
        HOST_DICT = {}
        HOST_KEYS = []
        for INVENTORY_VAL in INVENTORY.readlines():
            if re.search(r"\[.*\]", INVENTORY_VAL):
                INVENTORY_KEY = INVENTORY_VAL.strip("\n")
                HOST_KEYS.append(INVENTORY_KEY)
            elif re.findall(('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}'),INVENTORY_VAL):
                HOST_DICT.setdefault(INVENTORY_KEY, []).append(re.split(':', INVENTORY_VAL.strip("\n")))
            else:
                pass

        for HOST_KEYS_VAL in HOST_KEYS:
            if HOST_KEYS_VAL == "[gw]":
                threading.Thread(target=self.PUBLIC, name='recv',args=(HOST_DICT,HOST_KEYS_VAL)).start()
                #threading.Thread(target=self.GW, name='recv', args=(HOST_DICT, HOST_KEYS_VAL)).start()
            if HOST_KEYS_VAL == "[sio]":
                threading.Thread(target=self.PUBLIC, name='recv', args=(HOST_DICT, HOST_KEYS_VAL)).start()
                #threading.Thread(target=self.SIO, name='recv',args=(HOST_DICT,HOST_KEYS_VAL)).start()
            if HOST_KEYS_VAL == "[httpd]":
                threading.Thread(target=self.PUBLIC, name='recv', args=(HOST_DICT, HOST_KEYS_VAL)).start()
                #threading.Thread(target=self.HTTPD, name='recv',args=(HOST_DICT,HOST_KEYS_VAL)).start()
            if HOST_KEYS_VAL == "[nfs]":
                threading.Thread(target=self.PUBLIC, name='recv', args=(HOST_DICT, HOST_KEYS_VAL)).start()
                #threading.Thread(target=self.NFS, name='recv',args=(HOST_DICT,HOST_KEYS_VAL)).start()

if __name__ == '__main__':
    HOST()