#!/usr/local/bin/python

import socket

MAX_HOPS = 128
TIMEOUT = 5 # seconds
ICMP_CODE = socket.getprotobyname('icmp')
UDP_CODE = socket.getprotobyname('udp')

def ping(dest_name, ttl=30, port=33434):
    print ttl
    inn = socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP_CODE)
    out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, UDP_CODE)
    out.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
    inn.bind(("", port))
    inn.settimeout(TIMEOUT)
    out.sendto("", (dest_name, port))
    curr_addr = None
    curr_name = None
    try:
        _, curr_addr = inn.recvfrom(512)
        curr_addr = curr_addr[0]
        try:
            curr_name = socket.gethostbyaddr(curr_addr)[0]
        except socket.error:
            curr_name = curr_addr
    except socket.error:
        pass
    finally:
        out.close()
        inn.close()

    if curr_addr is not None:
        print "%s (%s)" % (curr_name, curr_addr)
    else:
        print "*"

    return curr_addr

def binary_search(host):
    ttl = MAX_HOPS / 2

    current = ping(host, ttl)

    while current != host:
        if current == None: # too high
            ttl /= 2
        else: # too low
            ttl += (MAX_HOPS - ttl)/2

        current = ping(host, ttl) # try again




def main(host):
    dest = socket.gethostbyname(host)
    binary_search(dest)
    # ttl = 1

    # while True:
    #     curr_addr = ping(dest_name, ttl)
    #     ttl += 1
    #     if curr_addr == dest or ttl >= MAX_HOPS:
    #         return

if __name__ == "__main__":
    main('www.mit.edu')
