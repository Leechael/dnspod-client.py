#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
Get Current IP then update target record(s).

Usage: ./dynamic_ip.py [record_id]
"""

import re
import os
from zlib import crc32
import requests
from dnspod_lib import *


def crc32b (data):
  return '%x' % (crc32(data), )

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
      old_ip = f.read().strip()
    if old_ip and old_ip == ip:
      exit(0)

  record = get_record(pattern)
  if record:
    update_record_ip(record, ip)
    with open('/tmp/dnspod_%s' % filename, 'w') as f:
      f.write(ip)
    print "Updated: %s now point to IP %s" % (pattern, ip)
    exit(0)

  print "Do nothing."
  exit(1)
