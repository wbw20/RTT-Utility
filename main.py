#!/usr/local/bin/python

import socket

MAX_HOPS = 30
ICMP_CODE = socket.getprotobyname('icmp')
UDP_CODE = socket.getprotobyname('udp')

def ping(dest_name, ttl=1, port=33434):
    inn = socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP_CODE)
    out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, UDP_CODE)
    out.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
    inn.bind(("", port))
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
        curr_host = "%s (%s)" % (curr_name, curr_addr)
    else:
        curr_host = "*"
    print "%d\t%s" % (ttl, curr_host)

    return curr_addr


def main(dest_name):
    dest_addr = socket.gethostbyname(dest_name)
    ttl = 1

    while True:
        curr_addr = ping(dest_name, ttl)
        ttl += 1
        if curr_addr == dest_addr or ttl >= MAX_HOPS:
            return

if __name__ == "__main__":
    main('www.mit.edu')
