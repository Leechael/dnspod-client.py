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
from dnspod_lib import *


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
