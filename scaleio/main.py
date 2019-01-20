#coding:utf-8

import socket
import threading
import time
import struct
import queue

queue = queue.Queue()

def udp_sender(ip,port):
    print(ip, port)
    try:
        ADDR = (ip,port)
        sock_udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sock_udp.sendto(b'abcd...',ADDR)
        sock_udp.close()
    except:
        pass

def icmp_receiver(ip,port):
    icmp = socket.IPPROTO_IP
    #icmp = socket.getprotobyname("icmp")
    try:
        sock_icmp = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    except socket.error as e:
        if e.errno == 1:
            # Operation not permitted
            msg = e.msg + (
                " - Note that ICMP messages can only be sent from processes"
                " running as root."
            )
            raise socket.error(msg)
        raise # raise the original error

    print("123")
    sock_icmp.settimeout(3)
    try:
        print(sock_icmp.recvfrom(64))
        recPacket,addr = sock_icmp.recvfrom(64)
    except:
        queue.put(True)
        return
    icmpHeader = recPacket[20:28]
    icmpPort = int(recPacket.encode('hex')[100:104],16)
    head_type, code, checksum, packetID, sequence = struct.unpack(
            "bbHHh", icmpHeader
    )
    sock_icmp.close()
    if code == 3 and icmpPort == port and addr[0] == ip:
        queue.put(False)
    return

def checker_udp(ip,port):
    thread_udp = threading.Thread(target=udp_sender,args=(ip,port))
    thread_icmp = threading.Thread(target=icmp_receiver,args=(ip,port))

    thread_udp.daemon= True
    thread_icmp.daemon = True

    thread_icmp.start()
    time.sleep(3)
    thread_udp.start()

    thread_icmp.join()
    thread_udp.join()
    return queue.get(False)

if __name__ == '__main__':
    print(checker_udp("192.168.1.109",162))