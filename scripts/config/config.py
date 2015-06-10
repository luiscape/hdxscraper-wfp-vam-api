#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import csv
import json

from os import path as p
from scripts.utilities.prompt_format import item

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
    print "Couldn't load configuration."
    print e
    return

  return data


def LoadEndpointInformation(endpoint, config):
  '''Loading information available for each endpoint.'''

  endpoint_names = [endpoints["name"] for endpoints in config['endpoints']]

  if endpoint not in endpoint_names:
    print "Endpoint not available."
    print "Available endpoints: " + ", ".join(endpoint_names) + "."
    return

  else:
    endpoints = config['endpoints']
    for e in endpoints:
      if e["name"] == endpoint:
        return e

