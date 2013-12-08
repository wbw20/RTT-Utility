#!/usr/local/bin/python

import socket
import time
import httplib
import json
from math import ceil, radians, cos, sin, asin, sqrt

MAX_HOPS = 32
TIMEOUT = 2 # seconds
ICMP_CODE = socket.getprotobyname('icmp')
UDP_CODE = socket.getprotobyname('udp')

def ping(dest_name, ttl=30, port=33434):
    inn = socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP_CODE)
    out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, UDP_CODE)
    out.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
    inn.bind(("", port))
    inn.settimeout(TIMEOUT)
    start = time.time()
    end = time.time() + TIMEOUT
    out.sendto("", (dest_name, port))
    curr_addr = None
    curr_name = None
    try:
        _, curr_addr = inn.recvfrom(512)
        end = time.time()
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

    return curr_addr, round((end - start)*1000)

def count_hops_to(host):
    low = 0
    high = MAX_HOPS
    ttl = 0

    while low < high:
        if ttl == (high + low)/2:
          break # don't run the same ttl twice
        else:
          ttl = (high + low)/2

        current, _ = ping(host, ttl) # try reaching host with ttl number of hops

        if current == None: # ttl too high
            high = ttl
        elif current.find(host) != -1: # ttl just right
            return ttl;
        else: # ttl too low
            low = ttl

    return low

def rtt_to(host, ttl):
  _, rtt = ping(host, ttl)
  return rtt

def geo_to(host):
  conn = httplib.HTTPConnection('freegeoip.net')

  conn.request('GET', '/json/%s' % (host))
  res =  json.loads(conn.getresponse().read())

  conn.request('GET', '/json/')
  me =  json.loads(conn.getresponse().read())

  conn.close()
  return haversine(float(res['latitude']), float(res['longitude']), float(me['latitude']), float(me['longitude']))

# This method is by Ross Allen, @ssorallen on github
def haversine(lon1, lat1, lon2, lat2):
  """
  Calculate the great circle distance between two points 
  on the earth (specified in decimal degrees)
  """
  # convert decimal degrees to radians 
  lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

  # haversine formula 
  dlon = lon2 - lon1 
  dlat = lat2 - lat1 
  a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
  c = 2 * asin(sqrt(a)) 

  # 6367 km is the radius of the Earth
  km = 6367 * c
  return int(km)


def main(host):
    dest = socket.gethostbyname(host)
    count = count_hops_to(dest)
    time = rtt_to(dest, count)
    geo = geo_to(dest)

    print "Hops to %s (%s)" % (host, count)
    print "RTT to %s (%s ms)" % (host, time)
    print "Distance to %s (%s km)\n" % (host, geo)

# run my trace and ping on each domain I was given in class
if __name__ == "__main__":
    for domain in ['ebay.com', 'amazon.cn', 'zendesk.com', 'toolband.com', 'att.com', 'rednet.cn', 'pornup.me', 'songofstyle.com', 'zackdougherty.com']:
        main(domain)
