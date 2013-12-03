#!/usr/local/bin/python

import socket
import struct

UDP_PROTOCOL_ID = 17 # RFC 768

def checksum(packet):
  """Add up the 1's compliment of the sum of 1's compliments for the packet"""

  sum = 0

  for x in packet:
    sum = sum + ~x
    sum = sum & 0xffffffff

  return ~sum

def to_i(ip):
  """Convert an ip address string to an int"""
  return int(''.join([bin(int(x)+256)[3:] for x in ip.split('.')]))

def create_packet(source, dest):
  """Creates a no-data UDP packet for the given source and destination."""

  # Pseudo header
  # source (32), destination (32), protocol (16), length (16)
  pseudo = [to_i(source), to_i(dest), UDP_PROTOCOL_ID, 8]

  return [to_i(source), to_i(dest), 8, checksum(pseudo)]

def ping(dest):
  print 'unused'

if __name__ == '__main__':
  print create_packet('192.168.1.1', '64.233.191.255')
