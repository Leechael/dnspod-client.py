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
import logging

import gevent
from gevent import monkey
monkey.patch_all()

import requests
from dnspod_lib import *


REGEX_IP=re.compile('(\d+\.\d+\.\d+\.\d+)')


def crc32b (data):
  hashed = '%x' % (crc32(data), )
  if hashed.startswith('-'):
    hashed = hashed[1:]
  return hashed


def read_cache (key):
  fn = '/tmp/dnspod_%s' % crc32b(key)
  if os.path.exists(fn):
    with open(fn, 'r') as f:
      data = f.read().strip().split(' ')
      print data
      if data and data[0]:
        expiry = int(data[0])
        if time.time() <= expiry:
          return data[1]
  return None


def write_cache (key, value, expiry=3600):
  fn = '/tmp/dnspod_%s' % crc32b(key)
  with open(fn, 'w') as f:
    f.write('%d %s' % (time.time()+expiry, value))
    return True
  return False


def fetch (url):
  resp = requests.get(url)
  if resp.ok:
    ips = REGEX_IP.findall(resp.content)
    return ips[0]
  return None


def get_ip (timeout=5):
  urls = (
      'http://checkip.dyndns.org/',
      'http://city.ip138.com/city.asp',
      )
  jobs = [gevent.spawn(fetch, url) for url in urls]
  gevent.joinall(jobs, timeout=timeout)
  for ip in [job.value for job in jobs]:
    if ip:
      return ip
  return None


if __name__ == '__main__':
  from sys import argv, exit
  if len(argv) < 2:
    print __doc__

  pattern = argv[1]
  logging.basicConfig(format='[%(asctime)-15s] [%(name)s] %(message)s',
      filename='/var/log/dnspod-client.log', level=logging.DEBUG)
  logger = logging.getLogger('dynamic_ip')

  ip = get_ip()
  if not ip:
    logger.critical('IP detects fault.')
    exit(1)

  prev = read_cache(pattern)
  if prev and prev == ip:
    logger.info('Lastest IP still fresh: %s' % ip)
    exit(0)

  record = get_record(pattern)
  if not record:
    logger.critical('Pattern `%s` has not match any exists record.' % pattern)
    exit(1)

  update_record_ip(record, ip)
  write_cache(pattern, ip)
  logging.info("Updated: %s now point to IP %s" % (pattern, ip))
