#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
------------------------------------------------------------------------------
Make sure you had been create config file before running this script.

Config file should locate in `~/.dnspodrc/config`, in format like:
"""
[common]
login_email = xxx
login_password = xxx
"""
------------------------------------------------------------------------------
'''

from time import sleep
from os import path
from ConfigParser import ConfigParser

import requests
from simplejson import loads as json_decode


class InvalidConfigError (BaseException):
  pass


# FIXME caching, caching!
def get_all_records ():
  domains = query('Domain.List', {'type': 'all'})['domains']
  groups = {}
  for domain in domains:
    did = domain['id']
    groups[did] = domain

    groups[did]['records'] = {};
    records = query('Record.List', {'domain_id': did})['records']
    for record in records:
      groups[did]['records'][record['id']] = record
      groups[did]['records'][record['id']]['domain_id'] = did
    sleep(0.3)
  return groups


def update_record_ip (record, ip):
  resp = query('Record.Modify', {
      'domain_id': record['domain_id'],
      'record_id': record['id'],
      'sub_domain': record['name'],
      'record_type': record['type'],
      'record_line': record['line'],
      'value': ip,
    }, False)
  msg = json_decode(resp.content)
  return msg


def query (path, params = {}, decode=True):
  defaults = {
      'format': 'json',
    }
  config = load_config()
  if not config:
    raise InvalidConfigError()
  if not 'common' in config and not 'login_email' in config['common'] and not 'login_password' in config['common']:
    raise InvalidConfigError()
  defaults.update(config['common'])
  params.update(defaults)

  headers = {
      'User-Agent': 'Weiwo SABot/1.0 (admin@meeit.com)',
    }

  domain = 'https://dnsapi.cn/'
  url = domain + path

  resp = requests.post(url, data=params, headers=headers)
  if not decode:
    return resp
  if resp.status_code != 200:
    # FIXME Error handling
    return False
  msg = json_decode(resp.content)
  if int(msg['status']['code']) != 1:
    # FIXME Error handling
    return False
  return msg


def load_config ():
  f = path.expanduser('~/.dnspodrc/config')
  returns = {}
  if path.exists(f):
    config = ConfigParser()
    config.read(f)
    for section in config.sections():
      returns[section] = {}
      for (k, v) in config.items(section):
        returns[section][k] = v
  return returns


if __name__ == '__main__':
  import sys
  if len(sys.argv) < 3:
    print "Usage: %s [search_ip] [replace_ip]" % (sys.argv[0])
    sys.exit(1)
  print __doc__
  search_ip = sys.argv[1]
  replace_ip = sys.argv[2]

  domains = get_all_records()
  for (domain_id, domain) in domains.items():
    print "Searching in domain `%s`..." % (domain['name'], )
    for (record_id, record) in domain['records'].items():
      if record['value'] == search_ip:
        print " Found: %s.%s - %s [%s, %s]" % (record['name'], domain['name'], record['value'], record['id'], record['type'])
        result = update_record_ip(record, replace_ip)
        print "   => Response status code: %s" % (result['status']['code'], )
