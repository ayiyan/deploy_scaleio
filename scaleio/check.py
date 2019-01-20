#!/usr/bin/env python
#coding=utf-8

from paramiko import SSHClient,AutoAddPolicy


class deploy:
    def __init__(self):
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect('127.0.0.1', port=7833, username='ericsson', password='ericsson')
        stdin, stdout, stderr = client.exec_command('ls /tmp/')
        value = stdout.read()
        print(value.decode())
        client.close()

if __name__ == '__main__':
    deploy()