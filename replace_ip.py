#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
------------------------------------------------------------------------------
Make sure you had been create config file before running this script.

Config file should locate in `~/.dnspodrc/config`, in format like:
"""
[common]
login_email = your_name@domain.com
login_password = password_not_using_to_login_csdn
"""
------------------------------------------------------------------------------
'''

from time import sleep
from os import path
from ConfigParser import ConfigParser

import requests
from simplejson import loads as json_decode


'''
Errors
'''
class InvalidConfigError (BaseException):
  pass

class RequestError (BaseException):
  pass

class ServiceError (BaseException):
  pass


'''
Functions
'''
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
  return query('Record.Modify', {
      'domain_id': record['domain_id'],
      'record_id': record['id'],
      'sub_domain': record['name'],
      'record_type': record['type'],
      'record_line': record['line'],
      'value': ip,
    })


def query (path, params = {}, decode=True):
  defaults = {
      'format': 'json',
    }
  config = load_config()
  defaults.update(config['common'])
  params.update(defaults)

  headers = {
      'User-Agent': 'Weiwo SABot/1.0 (yanleech@gmail.com)',
    }

  domain = 'https://dnsapi.cn/'
  url = domain + path

  resp = requests.post(url, data=params, headers=headers)
  if not decode:
    return resp
  if resp.status_code != 200:
    raise ServiceError("Got response status code `%s` but expected 200." % (resp.status_code, ))
  msg = json_decode(resp.content)
  if int(msg['status']['code']) != 1:
    raise RequestError("You just doing something DNSPod NOT allow: [%s] %s" % (msg['status']['code'], msg['status']['message']))
  return msg



CONFIG=None

def load_config ():
  if not globals()['CONFIG']:
    f = path.expanduser('~/.dnspodrc/config')
    returns = {}
    if path.exists(f):
      config = ConfigParser()
      config.read(f)
      for section in config.sections():
        returns[section] = {}
        for (k, v) in config.items(section):
          returns[section][k] = v
      if not 'common' in returns or not 'login_email' in returns['common'] or not 'login_password' in returns['common']:
        raise InvalidConfigError('One of following not providing in config: section `common`,  fields `login_email` or `login_password`.')
      globals()['CONFIG'] = returns
  if not returns:
    raise InvalidConfigError()
  return globals()['CONFIG']


'''
Worker.
'''
if __name__ == '__main__':
  import sys
  if len(sys.argv) < 3:
    print "Usage: %s [search_ip] [replace_ip]" % (sys.argv[0])
    sys.exit(1)

  search_ip = sys.argv[1]
  replace_ip = sys.argv[2]

  if not load_config():
    print __doc__
    sys.exit(1)

  domains = get_all_records()
  for (domain_id, domain) in domains.items():
    print "Searching in domain `%s`..." % (domain['name'], )
    for (record_id, record) in domain['records'].items():
      if record['value'] == search_ip:
        print " Found: %s.%s - %s [%s, %s]" % (record['name'], domain['name'], record['value'], record['id'], record['type'])
        result = update_record_ip(record, replace_ip)
        print "   => Response status code: %s" % (result['status']['code'], )
