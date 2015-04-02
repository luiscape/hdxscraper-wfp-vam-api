#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import csv
import json
import requests
import config as Config
from hdx_format import item
from store_records import StoreRecords

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]


def QueryWFP(endpoint, parameters, values, verbose = False, make_json = False, make_csv = False, store_db = True):
  '''Query WFP's CSI API.'''

  u = Config.BuildQueryString(endpoint, parameters, values)

  if verbose:
    print u
  
  r = requests.get(u)
  if r.status_code != 200:
    print "Query returned error code: %s" % r

  else:
    data = r.json()

    if len(data) == 0:
      print "%s Data not found for %s" % (item('prompt_bullet'), str(values[0]))

    if len(data) > 0:
      print "%s Data found for %s" % (item('prompt_bullet'), str(values[0]))

      if make_json:
        j_path = os.path.join(dir, 'data/') + endpoint + '_data_' + values[0] + '.json'
        with open(j_path, 'w') as outfile:
          json.dump(data, outfile)

      if make_csv:
        c_path = os.path.join(dir, 'data/') + endpoint + '_data_' + values[0] + '.csv'

        f = csv.writer(open(c_path, "wb+"))
        f.writerow(data[0].keys())

        for row in data:
          f.writerow([ row[key] if isinstance(row[key], dict) is False else row[key].values()[0] for key in row.keys() ])

      if store_db:
        for row in data:
          record = [{ key:row[key] if isinstance(row[key], dict) is False else row[key].values()[0] for key in row.keys() }]
          StoreRecords(record, endpoint)


def Main():
  '''Wrapper.'''

  c = Config.LoadListOfCountries()

  # for testing
  # c = [{
  #   'value': '239'
  # }]

  for country in c:
    parameters = ['adm0', 'indTypeID']
    values = [country['value'], '1']

    try:
      QueryWFP("FSC", parameters, values)
      QueryWFP("Income", parameters, values)

    except Exception as e:
      print e

    parameters_csi = ['adm0', 'indTypeID', 'type']
    values_csi = [country['value'], '1', 'r']

    try:
      QueryWFP("CSI", parameters_csi, values_csi)

    except Exception as e:
      print e




if __name__ == '__main__':
  Main()
