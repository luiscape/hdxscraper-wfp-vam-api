#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import csv
import json
# import requests
import grequests as requests
import scraperwiki
import config as Config
from hdx_format import item
from termcolor import colored as color
from store_records import StoreRecords

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]


def QueryWFP(url_list, verbose = False, make_json = True, make_csv = False, store_db = True, log = 'normal'):
  '''Query WFP's VAM API.'''

  if verbose:
    for url in url_list:
      print url

  def Handle(r, e):
    try:
      r
    except Exception as error:
      print "%s error with url %s" % (item('prompt_error'), r.status_code)
      print error

  request_list = (requests.get(url) for url in url_list)
  responses = requests.map(request_list, exception_handler=Handle)

  index = 1
  for r in responses:
    
    try:
      data = r.json()

    except Exception as e:
      if verbose:
        print "%s connection with the API failed." % item('promt_error')
    
    # info = [ key + '=' + parameters_dict[key] for key in parameters_dict.keys() ]
    # info_string = ", ".join(info)

    # if len(data) == 0:
    #   if log == 'scraperwiki':
    #     print "Data not found, %s" % (info_string)
    #   else:
    #     print "%s %s Data not found for %s" % (item('bullet_red'), color(endpoint, 'yellow'), info_string)

    # if len(data) > 0:
    #   if log == 'scraperwiki':
    #     "Data found, %s" % (info_string)

    if len(data) == 0:
      "Data not found"

    if len(data) > 0:
      print "%s %s Data found for %s" % (item('bullet_green'), color("TEST", 'yellow'), "TEST")

      if make_json:
        j_path = os.path.join(dir, 'data/') + "TEST" + '_data.json'
        with open(j_path, 'w') as outfile:
          json.dump(data, outfile)

      if make_csv:
        c_path = os.path.join(dir, 'data/') + "TEST" + '_data_.csv'

        f = csv.writer(open(c_path, "wb+"))
        f.writerow(data[0].keys())

        for row in data:
          f.writerow([ row[key] if isinstance(row[key], dict) is False else row[key].values()[0] for key in row.keys() ])

      if store_db:
        for row in data:
          record = [{ key:row[key] if isinstance(row[key], dict) is False else row[key].values()[0] for key in row.keys() }]
          StoreRecords(record, "TEST")


# def CreateUniqueCode():
  # '''Creating unique codes for locations.'''


def CreateURLArray(array, endpoint, parameters_dict):
  '''Creating an array of URLS to be passed to the async querier.'''
  u = Config.BuildQueryString(endpoint, parameters_dict)
  try:
    array.append(u)
  except Exception as e:
    print e


def BuildQueue(query_limit):
  '''Wrapper. query_limit determines the size of the url array.'''

  l = Config.LoadListOfLocations()
  url_list = []
  status = query_limit
  for row in l:
    if len(url_list) > query_limit:
      QueryWFP(url_list=url_list)
      p = round((float(status) / float(497680)) * 100, 2)
      print "%s progress: %s%%" % (item('prompt_bullet'), p)
      url_list = []
      status += query_limit

    parameters_dict = Config.RecurseDisagreggation(row=row)

    # for testing
    # parameters_dict = {'adm0': '239', 'indTypeID': '1'}

    # iterating over the type.
    type_ids = ['1', '2']
    csi_types = ['r', 'cs']
    for type in type_ids:
      parameters_dict["indTypeID"] = type

      try:

        # query Income and FSC
        CreateURLArray(array = url_list, endpoint = "FCS", parameters_dict = parameters_dict)
        CreateURLArray(array = url_list, endpoint = "Income", parameters_dict = parameters_dict)
        # QueryWFP("FCS", parameters_dict = parameters_dict)
        # QueryWFP("Income", parameters_dict = parameters_dict)

        # add extra parameter for CSI.
        for csi_type in csi_types:
          parameters_dict["type"] = csi_type
          # QueryWFP("CSI", parameters_dict = parameters_dict)
          CreateURLArray(array = url_list, endpoint = "CSI", parameters_dict = parameters_dict)

        parameters_dict.pop("type", None)  # deleting the entry

      except Exception as e:
        print "%s Connection failed." % item('prompt_error')




def Main():
  '''Wrapper.'''
  BuildQueue(query_limit=1000)

if __name__ == '__main__':

  try:
      Main()
      print "SW Status: Everything seems to be just fine."
      scraperwiki.status('ok')

  except Exception as e:
      print e
      scraperwiki.status('error', 'Error collecting data.')
      os.system("echo https://ds-ec2.scraperwiki.com/deudwxf/bfbenh2isykhn56/http/log.txt | mail -s 'WFP APIs: Failed collecting data.' luiscape@gmail.com")
