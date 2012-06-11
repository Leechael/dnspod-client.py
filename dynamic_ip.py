#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
Get Current IP then update target record(s).

Usage: ./dynamic_ip.py [record_id]
"""

import re
import os
from zlib import crc32
import time
import requests
from dnspod_lib import *


def crc32b (data):
  hashed = '%x' % (crc32(data), )
  if hashed.startswith('-'):
    hashed = hashed[1:]
  return hashed


def get_ip_by_dyndns ():
  resp = requests.get('http://checkip.dyndns.org/')
  ip = re.findall('(\d+\.\d+\.\d+\.\d+)', resp.content)
  return ip[0]


if __name__ == '__main__':
  from sys import argv, exit
  if len(argv) < 2:
    print __doc__

  pattern = argv[1]

  ip = get_ip_by_dyndns()
  filename = crc32b(pattern)
  if os.path.exists('/tmp/dnspod_%s' % filename):
    old_ip = None
    with open('/tmp/dnspod_%s' % filename, 'r') as f:
      data = f.read().strip().split(' ')
      expiry = int(data[0])
      old_ip = data[1]
    if time.time() <= expiry:
      if old_ip and old_ip == ip:
        exit(0)

  if True:
  #record = get_record(pattern)
  #if record:
    #update_record_ip(record, ip)
    with open('/tmp/dnspod_%s' % filename, 'w') as f:
      f.write("%s %s" % (time.time() + 600, ip))
    print "Updated: %s now point to IP %s" % (pattern, ip)
    exit(0)

  print "Do nothing."
  exit(1)
