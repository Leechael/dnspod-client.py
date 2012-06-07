#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from replace_ip import get_all_records

if __name__ == '__main__':
  for (domain_id, domain) in get_all_records().items():
    print 'Domain: `%s`' % (domain['name'], )
    for (record_id, record) in domain['records'].items():
      print '  => [%s] [%s] %s.%s - %s' % (record['id'], record['type'], record['name'], domain['name'], record['value'])
    print ''
