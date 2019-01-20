#!/usr/bin/env python
#coding=utf-8

import paramiko, os

SFTP = paramiko.Transport(('192.168.1.105', 22))
SFTP.connect(username='tux', password='ming')
SFTP_PUT = paramiko.SFTPClient.from_transport(SFTP)
SFTP_PUT.put('D:\Data\python\Ericsson\scaleio\main.py', '/home/tux/.ssh/main.py')
SFTP.close()