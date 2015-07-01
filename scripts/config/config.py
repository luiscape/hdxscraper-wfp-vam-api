#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import csv
import json

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

from utilities.prompt_format import item

def LoadConfig(j, verbose=False):
  '''Load configuration parameters.'''

  data_dir = os.path.split(dir)[0]

  try:
    j = os.path.join(data_dir, j)
    with open(j) as json_file:
      config = json.load(json_file)

  except Exception as e:
    print "%s Couldn't load list of locations: %s." % (item('prompt_error'), j)
    if verbose:
      print e
    return False

  return config

def LoadListOfLocations():
  '''Load list of countries.'''

  data_dir = os.path.split(dir)[0]

  config = LoadConfig(os.path.join(data_dir, 'config/config.json'))
  j = config['available_countries']

  try:
    j = os.path.join(data_dir, j)
    with open(j) as csv_file:
      data = csv.DictReader(csv_file)
      list_of_locations = []
      for row in data:
        list_of_locations.append(row)

  except Exception as e:
    print "%s Couldn't load list of locations: %s." % (item('prompt_error'), j)
    print e
    return False

  return list_of_locations


def LoadEndpointInformation(endpoint, verbose=False):
  '''Loading information available for each endpoint.'''

  data_dir = os.path.split(dir)[0]

  try:
    config = LoadConfig(os.path.join(data_dir, 'config', 'config.json'))

  except Exception as e:
    print "%s Couldn't load configuration file." % item('prompt_error')
    print e
    return False

  endpoint_names = []
  for endpoints in config['endpoints']:
    endpoint_names.append(endpoints["name"])

  if endpoint not in endpoint_names:
    print "Endpoint not available."
    print "Available endpoints: " + ", ".join(endpoint_names) + "."
    return Fale

  else:
    endpoints = config['endpoints']
    for e in endpoints:
      if e["name"] == endpoint:
        return e

