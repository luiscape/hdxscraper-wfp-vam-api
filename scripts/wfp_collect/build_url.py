#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import csv
import json

from scripts.config import config as Config


def AssembleLocationCodes(row):
  '''Collect the right parameters depending on the level of disaggregation.'''

  #
  # Assembling location codes.
  #
  location_codes = [
    {'level': 'adm%s' % level, 'code': row['ADM%s_CODE' % level]}
    for level in range(6) if len(row['ADM%s_CODE' % level])]

  #
  # Organizing output.
  #
  parameters = [parameter['level'] for parameter in location_codes]
  values = [value['code'] for value in location_codes]
  return dict(zip(parameters, values))


def BuildQueryString(endpoint_name, config, parameters_dict):
  '''Building the HTTP parameters.'''

  endpoint = Config.LoadEndpointInformation(endpoint_name, config['endpoints'])
  query_string = '?'

  for parameter, value in parameters_dict.items():
    if value and parameter not in endpoint['parameters']:
      print "Could not find parameter."
      return
    elif value:
      query_string += parameter + '=' + value + '&'

  return endpoint['url'] + query_string[:-1]
