#!/usr/bin/env python
# -*- encoding: utf-8 -*-

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
Config Loader
'''

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
  return globals()['CONFIG']


'''
Base RPC worker
'''
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
