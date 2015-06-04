#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

from config import config as Config

def SelectPreferedField(endpoint, nested_key):
  '''Selects a prefered frield from a key input and an endpoint.'''
  
  #
  # Load configuration endpoint.
  #
  e = Config.LoadEndpointInformation(endpoint)
  nested_keys = e['flattened_fields']

  #
  # Iterating over the fields.
  #
  for key in nested_keys:
    if key['nested_field'] == nested_key:
      return key['prefered_field']

  return 0


if __name__ == '__main__':
  print CheckSelected('CSI', 'TargetGroupR')