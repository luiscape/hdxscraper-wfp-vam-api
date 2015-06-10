#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import csv
import json

from os import path as p
from scripts.utilities.prompt_format import item

DATA_DIR = p.dirname(p.dirname(p.dirname(__file__)))
CONFIG_PATH = p.join(DATA_DIR, 'config', 'config.json')


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
      data = csv.DictReader(csv_file)
      list_of_locations = []
      for row in data:
        list_of_locations.append(row)

  except Exception as e:
    print "Couldn't load configuration."
    print e
    return

  return list_of_locations


def LoadEndpointInformation(endpoint):
  '''Loading information available for each endpoint.'''

  try:
    config = LoadConfig(CONFIG_PATH)

  except Exception as e:
    print "Couldn't load configuration file."
    print e
    return

  endpoint_names = []
  for endpoints in config['endpoints']:
    endpoint_names.append(endpoints["name"])

  if endpoint not in endpoint_names:
    print "Endpoint not available."
    print "Available endpoints: " + ", ".join(endpoint_names) + "."
    return

  else:
    endpoints = config['endpoints']
    for e in endpoints:
      if e["name"] == endpoint:
        return e

