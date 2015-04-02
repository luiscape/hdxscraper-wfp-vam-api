#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import requests

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

def LoadListOfCountries():
  '''Load list of countries.'''

  config = LoadConfig(os.path.join(dir, 'config/config.json'))
  j = config['available_countries']

  try:
    j = os.path.join(dir, j)
    with open(j) as json_file:    
      list_of_countries = json.load(json_file)

  except Exception as e:
    print "Couldn't load configuration."
    print e
    return

  return list_of_countries

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
    


def BuildQueryString(endpoint, parameters, values):
  '''Building the HTTP parameters.'''

  # try:
  #   config = LoadConfig(os.path.join(dir, 'config/config.json'))

  e = LoadEndpointInformation(endpoint)
  u = e['url']

  for parameter in parameters:
    if parameter not in e['parameters']:
      print "Could not find parameter."
      return

  parameters_dict = { parameter:value for parameter, value in zip(parameters, values) }
  
  query_string = '?'
  for p in parameters_dict.keys():
    query_string += p + '=' + parameters_dict[p] + '&'

  return u + query_string[:-1]