#!/usr/bin/env python
import socket
import struct
import sys
import threading
import time
import binascii

PACKETS_TO_RECEIVE = 25

# To work in Mininet routes must be configured for hosts similar to the following:
# route add -net 224.0.0.0/4 h1-eth0

multicast_group = '224.1.1.1'
multicast_port = 5007
echo_port = 5008

def main():
    global multicast_group, multicast_port
    
    if len(sys.argv) > 1:
        multicast_group = sys.argv[1]
    
    if len(sys.argv) > 2:
        multicast_port = sys.argv[2]
    
    # Setup the socket for receive multicast traffic
    multicast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    multicast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    multicast_socket.bind(('', multicast_port))
    mreq = struct.pack("=4sl", socket.inet_aton(multicast_group), socket.INADDR_ANY)
    multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    # Setup the socket for sending echo response
    echo_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    recv_packets = 0
    while True:
        try:
            data, addr = multicast_socket.recvfrom(128)
            echo_socket.sendto(data, (addr[0], echo_port))
            print 'Echo packet ' + str(int(data)) + ' to ' + str(addr[0]) + ':' + str(echo_port)
            recv_packets += 1
        except socket.error, e:
            print 'Exception'
        
        if recv_packets > PACKETS_TO_RECEIVE:
            break
    
    multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)
    
if __name__ == '__main__':
    main()