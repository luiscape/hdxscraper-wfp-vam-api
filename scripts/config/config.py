#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import csv
import json

# Below as a helper for namespaces.
# Looks like a horrible hack.
dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

from os import path as p
from utilities.prompt_format import item

DATA_DIR = p.dirname(p.dirname(p.dirname(__file__)))
CONFIG_PATH = p.join(DATA_DIR, 'config', 'config.json')
DEV_CONFIG_PATH = p.join(DATA_DIR, 'config', 'dev_config.json')


def LoadConfig(config_path, verbose=False):
  '''Load configuration parameters.'''

  try:
    with open(config_path) as json_file:
      config = json.load(json_file)

  except Exception as e:
    print "%s Couldn't load configuration." % item('prompt_error')
    if verbose:
      print e
    return False

  return config


def LoadListOfLocations(config):
  '''Load list of countries.'''

  country_path = config['available_countries']

  try:
    c_path = p.join(DATA_DIR, country_path)

    with open(c_path) as csv_file:
      data = [row for row in csv.DictReader(csv_file)]

  except Exception as e:
    print "%s Couldn't load configuration." % item('prompt_error')
    print e
    return

  return data


def LoadEndpointInformation(name, endpoints):
  '''Loading information available for each endpoint.'''
  try:
    endpoint = [e for e in endpoints if e['name'] == name][0]
  except IndexError:
    endpoint = None
    print 'Endpoint %s not available.' % name
    print 'Available endpoints: %s.' % ', '.join(e['name'] for e in endpoints)

  return endpoint
