#!/usr/bin/env python
#coding=utf-8

import os
import re
import threading
from paramiko import SSHClient, AutoAddPolicy, SFTPClient

class SERVER(threading.Thread):
    def __init__(self, IPADDRESS, PORT):
        #print(os.getppid(), os.getpid())
        threading.Thread.__init__(self)
        self.IPADDRESS = IPADDRESS
        self.PORT = PORT

    def run(self):
        COMMAND_LIST = [
            'systemctl stop iptables.service',
            'hostname'
        ]
        CLIENT = SSHClient()
        CLIENT.set_missing_host_key_policy(AutoAddPolicy())
        CLIENT.connect(self.IPADDRESS, port=self.PORT, username='ericsson', password='ericsson')
        stdin, stdout, stderr = CLIENT.exec_command('mkdir -p mkdir -p /tmp/deploy_ming/{software,shell,template}')
        os.system('pause')
        for COMMAND_LIST_VAL in COMMAND_LIST:
            stdin, stdout, stderr = CLIENT.exec_command(COMMAND_LIST)
        sftp = SFTPClient.from_transport(CLIENT)
        sftp.put("software/*.rar", "/tmp/deploy_ming/software")
        value = stdout.read()
        print(self.PORT, bytes.decode(value))
        CLIENT.close()
        return value.decode()


class HOST(SERVER):
    def __init__(self):
        self.RUN()

    def RUN(self):
        INVENTORY = open('config\inventory')
        HOST_DICT = {}
        HOST_KEYS = []
        for INVENTORY_VAL in INVENTORY.readlines():
            #print(INVENTORY_VAL)
            if re.search(r"\[.*\]", INVENTORY_VAL):
                INVENTORY_KEY = INVENTORY_VAL.strip("\n")
                HOST_KEYS.append(INVENTORY_KEY)
            elif re.findall(('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}'),INVENTORY_VAL):
                HOST_DICT.setdefault(INVENTORY_KEY, []).append(re.split(':', INVENTORY_VAL.strip("\n")))
            else:
                pass

        for HOST_KEYS_VAL in HOST_KEYS:
            if HOST_KEYS_VAL == "[gw]":
                for GW_LIST in HOST_DICT[HOST_KEYS_VAL]:
                    IPADDRESS = GW_LIST[0]
                    PORT = GW_LIST[1]
                    GW_THREAD = SERVER(IPADDRESS, PORT)
                    GW_THREAD.start()
                    #print(os.getppid(), os.getpid())
            elif HOST_KEYS_VAL == "[httpd]":
                for HTTPD_LIST in HOST_DICT[HOST_KEYS_VAL]:
                    IPADDRESS = HTTPD_LIST[0]
                    PORT = HTTPD_LIST[1]
                    HTTPD_THREAD = SERVER2(IPADDRESS, PORT)
                    HTTPD_THREAD.start()
            elif HOST_KEYS_VAL == "[nfs]":
                for NFS_LIST in HOST_DICT[HOST_KEYS_VAL]:
                    IPADDRESS = NFS_LIST[0]
                    PORT = NFS_LIST[1]
                    NFS_THREAD = SERVER3(IPADDRESS, PORT)
                    NFS_THREAD.start()
            elif HOST_KEYS_VAL == "[sio]":
                for SIO_LIST in HOST_DICT[HOST_KEYS_VAL]:
                    IPADDRESS = SIO_LIST[0]
                    PORT = SIO_LIST[1]
                    SIO_THREAD = SERVER(IPADDRESS, PORT)
                    SIO_THREAD.start()
            else:
                pass

if __name__ == '__main__':
    HOST()