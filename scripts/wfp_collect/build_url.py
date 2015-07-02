#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

# Below as a helper for namespaces.
# Looks like a horrible hack.
dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

import csv
import json

from config import config as Config

def AssembleLocationCodes(row):
  '''Collect the right parameters depending on the level of disaggregation.'''

  #
  # What levels should be collected.
  #
  levels = [0,1,2,3,4,5]

  #
  # Assembling location codes.
  #
  location_codes = []
  for level in levels:
    level_name = 'ADM{0}_CODE'.format(level,)
    parameter_name = 'adm{0}'.format(level,)
    if len(row[level_name]) > 0:
      location_codes.append({
        "level": parameter_name,
        "code": row[level_name]
        })

  #
  # Organizing output.
  #
  parameters = [ parameter['level'] for parameter in location_codes ]
  values = [ value['code'] for value in location_codes ]
  output = { parameter:value for parameter,value in zip(parameters, values) }
  return output


def BuildQueryString(endpoint, parameters_dict):
  '''Building the HTTP parameters.'''

  e = Config.LoadEndpointInformation(endpoint)
  u = e['url']

  for parameter in parameters_dict.keys():
    if parameter not in e['parameters']:
      print "Could not find parameter."
      return False

  query_string = '?'
  for p in parameters_dict.keys():
    query_string += p + '=' + parameters_dict[p] + '&'

  return u + query_string[:-1]


