#!/usr/bin/env python
#coding=utf-8

import os
import re
import time
import threading
from paramiko import SSHClient, AutoAddPolicy, SFTPClient, Transport

class HOST:
    def __init__(self):
        self.RUN()

    def CONNECTION(self):
        IPADDRESS = GW_LIST[0]
        PORT = GW_LIST[1]
        USERNAME = GW_LIST[2]
        PASSWORD = GW_LIST[3]
        self.CLIENT = SSHClient()
        self.CLIENT.set_missing_host_key_policy(AutoAddPolicy())
        self.CLIENT.connect(IPADDRESS, port=PORT, username=USERNAME, password=PASSWORD) 

        
    def HTTPD(self,HOST_DICT,HOST_KEYS_VAL):
        for GW_LIST in HOST_DICT[HOST_KEYS_VAL]:  
            pass


    @CONNECTION
    def PUBLIC(self, self.HOST_DICT,self.HOST_KEYS_VAL):
        COUNTER=0
        for GW_LIST in HOST_DICT[HOST_KEYS_VAL]:
            COUNTER += 1
            IPADDRESS = GW_LIST[0]
            PORT = GW_LIST[1]
            USERNAME = GW_LIST[2]
            PASSWORD = GW_LIST[3]
            CLIENT = SSHClient()
            CLIENT.set_missing_host_key_policy(AutoAddPolicy())
            CLIENT.connect(IPADDRESS, port=PORT, username=USERNAME, password=PASSWORD) 

            # Check Get Hostname
            stdin, stdout, stderr = CLIENT.exec_command('hostname')
            HOSTNAME_VAL = (bytes.decode(stdout.read())).strip()
            #print("%s %s "%(HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"), HOSTNAME_VAL))

            # Check PING TEST DNS&ECAS
            # stdin, stdout, stderr = CLIENT.exec_command('/usr/sbin/ip addr | grep -v mdm | grep -o -P "(\d+\.)(\d+\.)(\d+\.)(\d+)/25" |grep -v -E "127.|192."')
            # IPADDRESS_VAL= (bytes.decode(stdout.read()).replace('/25','').strip('\n'))
            # stdin, stdout, stderr = CLIENT.exec_command('ping -c 1 192.168.87.248 > /dev/null   && echo 0 || echo 1')
            # PING_VAL1 = bytes.decode(stdout.read())
            # if int(PING_VAL1) == 0:
            #     print("%s %s Ping 192.168.87.248 is: ---> \033[32m[OK]\033[0m"%(HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"), IPADDRESS_VAL))
            # else:
            #     print("%s %s Ping 192.168.87.248 is: ---> \033[31m[Failed]\033[0m"%(HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"), IPADDRESS_VAL))
            # stdin, stdout, stderr = CLIENT.exec_command('ping -c 1 192.168.187.248 > /dev/null   && echo 0 || echo 1')
            # PING_VAL2 = bytes.decode(stdout.read())
            # if int(PING_VAL2) == 0:
            #     print("%s %s Ping 192.168.187.248 is: ---> \033[32m[OK]\033[0m"%(HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"), IPADDRESS_VAL))
            # else:
            #     print("%s %s Ping 192.168.187.248 is: ---> \033[31m[Failed]\033[0m"%(HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"), IPADDRESS_VAL))
            # stdin, stdout, stderr = CLIENT.exec_command('ping -c 1 192.168.15.20 > /dev/null   && echo 0 || echo 1')
            # PING_VAL3 = bytes.decode(stdout.read())
            # if int(PING_VAL3) == 0:
            #     print("%s %s Ping 192.168.15.20 is: ---> \033[32m[OK]\033[0m"%(HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"), IPADDRESS_VAL))
            # else:
            #     print("%s %s Ping 192.168.15.20 is: ---> \033[31m[Failed]\033[0m"%(HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"), IPADDRESS_VAL))

            # Check PermitRoot yes--->no
            #stdin, stdout, stderr = CLIENT.exec_command('sudo sed -i.bak  "s/^PermitRootLogin yes/PermitRootLogin no/g" /etc/ssh/sshd_config')
            #FIREWALL_VAL= bytes.decode(stdout.read())
            #stdin, stdout, stderr = CLIENT.exec_command('sudo systemctl restart sshd')

            #/etc/resoly.conf
            # stdin, stdout, stderr = CLIENT.exec_command('sudo cat /etc/resolv.conf | grep search')
            # DOMAIN_VAL = bytes.decode(stdout.read())
            # print(HOSTNAME_VAL,"--->",DOMAIN_VAL)

            # Check iptables
            # stdin, stdout, stderr = CLIENT.exec_command('sudo systemctl is-active iptables')
            # FIREWALL_VAL= bytes.decode(stdout.read())
            # if FIREWALL_VAL.strip() == "active":
            #     print("%s FireWall ---> \033[32m[Open]\033[0m"%(HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"), HOSTNAME_VAL))
            # else:
            #     print("%s FireWall ---> \033[31m[Close]\033[0m"%(HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"), HOSTNAME_VAL))

            # Check RootLogin
            # stdin, stdout, stderr = CLIENT.exec_command("sudo grep -i ^PermitRootLogin /etc/ssh/sshd_config | awk '{print $2}'")
            # ROOTLOGIN_VAL= bytes.decode(stdout.read())
            # if ROOTLOGIN_VAL.strip() == "no":
            #     print("%s PermitRootLogin ---> \033[32m[Closed]\033[0m"%(HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"), HOSTNAME_VAL))
            # else:
            #     print("%s PermitRootLogin ---> \033[31m[Active]\033[0m"%(HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"), HOSTNAME_VAL))

            # Check Port:80
            stdin, stdout, stderr = CLIENT.exec_command("sudo lsof -i :80")
            HTTPPORT_VAL= bytes.decode(stdout.read())
            if HTTPPORT_VAL.strip() == "":
                print("%s %s HTTPPORT ---> \033[32m[Closed]\033[0m"%(HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"), HOSTNAME_VAL))
            else:
                print("%s %s HTTPPORT ---> \033[31m[Open]\033[0m"%(HOST_KEYS_VAL.replace("]",str(COUNTER)+"]"), HOSTNAME_VAL))


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
                #self.PUBLIC(HOST_DICT, HOST_KEYS_VAL)
                threading.Thread(target=self.PUBLIC, name='recv',args=(HOST_DICT,HOST_KEYS_VAL)).start()
            if HOST_KEYS_VAL == "[sio]":
                #self.PUBLIC(HOST_DICT, HOST_KEYS_VAL)
                threading.Thread(target=self.PUBLIC, name='recv', args=(HOST_DICT, HOST_KEYS_VAL)).start()
            if HOST_KEYS_VAL == "[httpd]":
                #self.PUBLIC(HOST_DICT, HOST_KEYS_VAL)
                threading.Thread(target=self.PUBLIC, name='recv', args=(HOST_DICT, HOST_KEYS_VAL)).start()
            if HOST_KEYS_VAL == "[nfs]":
                #self.PUBLIC(HOST_DICT, HOST_KEYS_VAL)
                threading.Thread(target=self.PUBLIC, name='recv', args=(HOST_DICT, HOST_KEYS_VAL)).start()
if __name__ == '__main__':
    HOST()