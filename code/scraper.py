#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import csv
import json
import requests
import config as Config
from hdx_format import item
from termcolor import colored as color
from store_records import StoreRecords

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]


def QueryWFP(endpoint, parameters_dict, verbose = False, make_json = False, make_csv = False, store_db = True):
  '''Query WFP's VAM API.'''

  u = Config.BuildQueryString(endpoint, parameters_dict)

  if verbose:
    print u
  
  r = requests.get(u)
  if r.status_code != 200:
    print "Query returned error code: %s" % r

  else:
    data = r.json()
    info = [ key + '=' + parameters_dict[key] for key in parameters_dict.keys() ]
    info_string = ", ".join(info)

    if len(data) == 0:
      print "%s %s Data not found for %s" % (item('bullet_red'), color(endpoint, 'yellow'), info_string)

    if len(data) > 0:
      print "%s %s Data found for %s" % (item('bullet_green'), color(endpoint, 'yellow'), info_string)

      if make_json:
        j_path = os.path.join(dir, 'data/') + endpoint + '_data.json'
        with open(j_path, 'w') as outfile:
          json.dump(data, outfile)

      if make_csv:
        c_path = os.path.join(dir, 'data/') + endpoint + '_data_.csv'

        f = csv.writer(open(c_path, "wb+"))
        f.writerow(data[0].keys())

        for row in data:
          f.writerow([ row[key] if isinstance(row[key], dict) is False else row[key].values()[0] for key in row.keys() ])

      if store_db:
        for row in data:
          record = [{ key:row[key] if isinstance(row[key], dict) is False else row[key].values()[0] for key in row.keys() }]
          StoreRecords(record, endpoint)


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


# def CreateUniqueCode():
  # '''Creating unique codes for locations.'''

def Main():
  '''Wrapper.'''

  l = Config.LoadListOfLocations()
  for row in l:
    parameters_dict = RecurseDisagreggation(row=row)
    parameters_dict["indTypeID"] = '1'

    # query Income and FSC
    QueryWFP("Income", parameters_dict = parameters_dict)
    QueryWFP("FSC", parameters_dict = parameters_dict)

    # add extra parameter for CSI
    parameters_dict["type"] = 'r'
    QueryWFP("CSI", parameters_dict = parameters_dict)



if __name__ == '__main__':

  try:
      Main()
      print "SW Status: Everything seems to be just fine."
      scraperwiki.status('ok')

  except Exception as e:
      print e
      scraperwiki.status('error', 'Error collecting data.')
      os.system("echo https://ds-ec2.scraperwiki.com/deudwxf/bfbenh2isykhn56/http/log.txt | mail -s 'WFP APIs: Failed collecting data.' luiscape@gmail.com")
