#!/usr/local/bin/python

import socket
import struct

UDP_PROTOCOL_ID = 17 # RFC 768

def checksum(packet):
  """Calculate the checksum of the combined UDP and IP pseudoheader according to RFC 768."""

  print(len(packet))

def to_i(ip):
  """Convert an ip address string to an int"""
  return struct.unpack("!I", socket.inet_aton(ip))[0]

def create_packet(source, dest):
  """Creates a no-data UDP packet for the given source and destination."""

  # Pseudo header
  # source (32), destination (32), protocol (16), length (16)
  pseudo = struct.pack('IIhh', source, dest, UDP_PROTOCOL_ID, 8)

  # Return our actual checksum
  # source (32), destination (32), length(16), checksum (16)
  return struct.pack('IIhh', source, dest, 8, checksum(pseudo))

def ping(dest):
  print 'unused'

if __name__ == '__main__':
  print to_i('192.168.1.1')
  create_packet(to_i('127.0.0.1'), to_i('64.233.191.255')) # test ping
