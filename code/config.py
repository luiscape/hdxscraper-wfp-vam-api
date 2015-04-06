#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import csv
import json
import requests
from termcolor import colored as color

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]

def LoadConfig(j):
  '''Load configuration parameters.'''
  try:
    j = os.path.join(dir, j)
    with open(j) as json_file:    
      config = json.load(json_file)

  except Exception as e:
    print "Couldn't load configuration."
    print e
    return

  return config

def LoadListOfLocations():
  '''Load list of countries.'''

  config = LoadConfig(os.path.join(dir, 'config/config.json'))
  j = config['available_countries']

  try:
    j = os.path.join(dir, j)
    # with open(j) as json_file:    
    #   list_of_countries = json.load(json_file)
    with open(j) as csv_file:
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
    config = LoadConfig(os.path.join(dir, 'config/config.json'))

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
    
def RecurseDisagreggation(row):
  '''Collect the right parameters depending on the level of disaggregation.'''

  # administrative levels
  levels = [0,1,2,3,4,5]

  location_codes = []
  for level in levels:
    level_name = 'ADM{0}_CODE'.format(level,)
    parameter_name = 'adm{0}'.format(level,)
    if len(row[level_name]) > 0:
      location_codes.append({
        "level": parameter_name,
        "code": row[level_name] 
        })

  # some lovely list comprehension
  parameters = [ parameter['level'] for parameter in location_codes ]
  values = [ value['code'] for value in location_codes ]
  output = { parameter:value for parameter,value in zip(parameters, values) }
  return output


def BuildQueryString(endpoint, parameters_dict):
  '''Building the HTTP parameters.'''

  e = LoadEndpointInformation(endpoint)
  u = e['url']

  for parameter in parameters_dict.keys():
    if parameter not in e['parameters']:
      print "Could not find parameter."
      return
  
  query_string = '?'
  for p in parameters_dict.keys():
    query_string += p + '=' + parameters_dict[p] + '&'

  return u + query_string[:-1]