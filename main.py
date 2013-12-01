#!/usr/local/bin/python

UDP_PROTOCOL_ID = 17 # RFC 768

def checksum(packet):
  """Calculate the checksum of the combined UDP and IP pseudoheader according to RFC 768."""

def create_packet(source, dest):
  """Creates a no-data UDP packet for the given source and destination."""

  # Pseudo header
  # source (32), destination (32), protocol (16), length (16)
  pseudo = struct.pack(source, dest, UDP_PROTOCOL_ID, 8)

  # Return our actual checksum
  # source (32), destination (32), length(16), checksum (16)
  return struct.pack(source, dest, 8, checksum(pseudo))

def ping(dest):

if __name__ == '__main__':
  # ping('google.com')
