#!/usr/bin/env python
#coding=utf-8

import os
import re
import time
import threading
from paramiko import SSHClient, AutoAddPolicy, SFTPClient, Transport

class SERVER(threading.Thread):
    def __init__(self, HOST_KEYS_VAL, IPADDRESS, PORT, COUNT_NUM, USERNAME, PASSWORD):
        #print(os.getppid(), os.getpid())
        threading.Thread.__init__(self)
        self.IPADDRESS = IPADDRESS
        self.PORT = PORT
        self.HOST_KEYS_VAL = HOST_KEYS_VAL
        self.COUNT_NUM = COUNT_NUM
        self.USERNAME = USERNAME
        self.PASSWORD = PASSWORD

    def run(self):
        COMMAND_LIST = [
            'sudo systemctl stop iptables.service',
            'mkdir -p mkdir -p /tmp/deploy_ming/{config,software,shell,template,log}'
        ]
        CLIENT = SSHClient()
        CLIENT.set_missing_host_key_policy(AutoAddPolicy())
        CLIENT.connect(self.IPADDRESS, port=self.PORT, username=self.USERNAME, password=self.PASSWORD)
        stdin, stdout, stderr = CLIENT.exec_command('hostname')
        value = stdout.read()
        HOSTNAME_VAL= bytes.decode(value)
        HOSTLIST = open("config/hostlist", 'a')
        HOSTLIST.writelines("%s:%s:%s" % (self.HOST_KEYS_VAL,HOSTNAME_VAL.strip('\n'),self.IPADDRESS)+"\n")
        HOSTLIST.close()

        HOSTCOUNT=0
        HOSTLIST = open("config/hostlist", 'r')
        while True:
            for HOSTLIST_VAL in HOSTLIST.readlines():
                if re.findall(('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'), HOSTLIST_VAL):
                    HOSTCOUNT+=1
            if HOSTCOUNT == self.COUNT_NUM:
                break
            else:
                time.sleep(3)
        HOSTLIST.close()


        for COMMAND_LIST_VAL in COMMAND_LIST:
            stdin, stdout, stderr = CLIENT.exec_command(COMMAND_LIST_VAL)

        SFTP = Transport((self.IPADDRESS, int(self.PORT)))
        SFTP.connect(username='tux', password='ming')
        SFTP_PUT = SFTPClient.from_transport(SFTP)
        SFTP_PUT.put('config/id_rsa', '/tmp/deploy_ming/config/id_rsa')
        SFTP_PUT.put('config/hostlist', '/tmp/deploy_ming/config/hostlist')
        SFTP_PUT.put('config/ip_val', '/tmp/deploy_ming/config/ip_val')
        SFTP_PUT.put('template/keepalived.conf', '/tmp/deploy_ming/template/keepalived.conf')
        SFTP_PUT.put('template/mod_jk.conf', '/tmp/deploy_ming/template/mod_jk.conf')
        SFTP_PUT.put('template/workers.properties', '/tmp/deploy_ming/template/workers.properties')
        SFTP_PUT.put('shell/gw.sh', '/tmp/deploy_ming/shell/gw.sh')
        SFTP_PUT.put('shell/httpd.sh', '/tmp/deploy_ming/shell/httpd.sh')
        SFTP_PUT.put('shell/sio.sh', '/tmp/deploy_ming/shell/sio.sh')
        SFTP_PUT.close()
        stdin, stdout, stderr = CLIENT.exec_command('chmod +x /tmp/deploy_ming/shell/*.sh')
        stdin, stdout, stderr = CLIENT.exec_command('chmod 600 /tmp/deploy_ming/config/id_rsa')
        #print(self.HOST_KEYS_VAL)
        if "sio" in self.HOST_KEYS_VAL:
            pass
            # stdin, stdout, stderr = CLIENT.exec_command("cd /tmp/deploy_ming/shell/;nohup ./sio.sh &")
        elif "gw" in self.HOST_KEYS_VAL:
            pass
            # stdin, stdout, stderr = CLIENT.exec_command("cd /tmp/deploy_ming/shell/;nohup ./gw.sh &")
        elif "httpd" in self.HOST_KEYS_VAL:
            print(self.HOST_KEYS_VAL)
            stdin, stdout, stderr = CLIENT.exec_command("cd /tmp/deploy_ming/shell/;nohup ./httpd.sh &")
        else:
            pass
        CLIENT.close()


class HOST(SERVER):
    def __init__(self):
        self.RUN()

    def RUN(self):
        CLEAR_HOSTLIST = open('config\hostlist','w+')
        CLEAR_HOSTLIST.truncate()
        CLEAR_HOSTLIST.close()

        INVENTORY = open('config\inventory')
        HOST_DICT = {}
        HOST_KEYS = []
        COUNT_NUM=0
        for INVENTORY_VAL in INVENTORY.readlines():
            #print(INVENTORY_VAL)
            if re.search(r"\[.*\]", INVENTORY_VAL):
                INVENTORY_KEY = INVENTORY_VAL.strip("\n")
                HOST_KEYS.append(INVENTORY_KEY)
            elif re.findall(('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}'),INVENTORY_VAL):
                HOST_DICT.setdefault(INVENTORY_KEY, []).append(re.split(':', INVENTORY_VAL.strip("\n")))
                COUNT_NUM+=1
            else:
                pass

        #print(COUNT_NUM)


        for HOST_KEYS_VAL in HOST_KEYS:
            if HOST_KEYS_VAL == "[gw]":
                SEQ = 0
                for GW_LIST in HOST_DICT[HOST_KEYS_VAL]:
                    SEQ+=1
                    IPADDRESS = GW_LIST[0]
                    PORT = GW_LIST[1]
                    USERNAME = GW_LIST[2]
                    PASSWORD = GW_LIST[3]
                    GW_THREAD = SERVER(HOST_KEYS_VAL.replace(']',str(SEQ)+']'), IPADDRESS, PORT, COUNT_NUM, USERNAME, PASSWORD)
                    GW_THREAD.start()                 
                    #print(os.getppid(), os.getpid())
            elif HOST_KEYS_VAL == "[httpd]":
                SEQ = 0
                for HTTPD_LIST in HOST_DICT[HOST_KEYS_VAL]:
                    SEQ+=1
                    IPADDRESS = HTTPD_LIST[0]
                    PORT = HTTPD_LIST[1]
                    USERNAME = GW_LIST[2]
                    PASSWORD = GW_LIST[3]
                    HTTPD_THREAD = SERVER(HOST_KEYS_VAL.replace(']',str(SEQ)+']'), IPADDRESS, PORT, COUNT_NUM, USERNAME, PASSWORD)
                    HTTPD_THREAD.start()  
            elif HOST_KEYS_VAL == "[nfs]":
                SEQ = 0
                for NFS_LIST in HOST_DICT[HOST_KEYS_VAL]:
                    SEQ+=1
                    IPADDRESS = NFS_LIST[0]
                    PORT = NFS_LIST[1]
                    USERNAME = GW_LIST[2]
                    PASSWORD = GW_LIST[3]
                    NFS_THREAD = SERVER(HOST_KEYS_VAL.replace(']',str(SEQ)+']'), IPADDRESS, PORT, COUNT_NUM, USERNAME, PASSWORD)
                    NFS_THREAD.start()
            elif HOST_KEYS_VAL == "[sio]":
                SEQ = 0
                for SIO_LIST in HOST_DICT[HOST_KEYS_VAL]:
                    SEQ+=1
                    IPADDRESS = SIO_LIST[0]
                    USERNAME = GW_LIST[2]
                    PASSWORD = GW_LIST[3]
                    PORT = SIO_LIST[1]
                    SIO_THREAD = SERVER(HOST_KEYS_VAL.replace(']',str(SEQ)+']'), IPADDRESS, PORT, COUNT_NUM, USERNAME, PASSWORD)
                    SIO_THREAD.start()
            else:
                pass

if __name__ == '__main__':
    HOST()