#!/usr/local/bin/python

import socket
import struct

UDP_PROTOCOL_ID = 17 # RFC 768

def checksum(packet):
  """Calculate the checksum of the combined UDP and IP pseudoheader according to RFC 768."""

def to_b(ip):
  """Convert an ip address string to a binary"""
  return ''.join([bin(int(x)+256)[3:] for x in ip.split('.')])

def create_packet(source, dest):
  """Creates a no-data UDP packet for the given source and destination."""

  # Pseudo header
  # source (32), destination (32), protocol (16), length (16)
  pseudo = struct.pack('IIhh', source, dest, UDP_PROTOCOL_ID, 8)

  print(checksum(pseudo))

  # Return our actual checksum
  # source (32), destination (32), length(16), checksum (16)
  return struct.pack('IIhh', source, dest, 8, checksum(pseudo))

def ping(dest):
  print 'unused'

if __name__ == '__main__':
  print to_b('192.168.1.1')
