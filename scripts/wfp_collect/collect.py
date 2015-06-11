#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import csv
import json
import scraperwiki
import progressbar as pb
import grequests as requests

from os import path as p
from math import ceil
from scripts.config import config as Config
from scripts.utilities import db
from scripts.utilities.prompt_format import item
from scripts.utilities.store_records import StoreRecords
from scripts.wfp_collect.build_url import AssembleLocationCodes
from scripts.wfp_collect.build_url import BuildQueryString


def flatten_row(row, preferred_fields):
  for key, value in row.items():
    preferred_field = preferred_fields.get(key, {}).get('preferred_field')

    try:
      # Flatten based on preferred key from the config file.
      # If config file didn't list a preferred key, the use the first field.
      preferred_field = preferred_field or value.keys(0)
    except AttributeError:
      # value isn't nested
      pass

    row[key] = value[preferred_field] if preferred_field else value

  return row


def QueryWFP(url_list, db_table, endpoint_info, **kwargs):
  '''Query WFP's VAM API asynchronously.'''
  data_dir = kwargs['data_dir']
  verbose = kwargs.get('verbose')
  make_json = kwargs.get('make_json')
  make_csv = kwargs.get('make_csv')
  store_db = kwargs.get('store_db', True)

  #
  # Load endpoint information.
  #
  preferred_fields = endpoint_info['preferred_fields']

  if verbose:
    for url in url_list:
      print '%s query: %s' % (item('prompt_bullet'), url)

  #
  # Defining the asynchronous request.
  #
  def _handle(r, e):
    try:
      r
    except Exception as error:
      print "%s error with URL %s" % (item('prompt_error'), r.status_code)
      print error

  request_list = (requests.get(url) for url in url_list)
  responses = requests.map(request_list, exception_handler=_handle)

  for index, r in enumerate(responses, 1):
    data = r.json() if r else []
    length = len(data)

    #
    # Check if there is data available and store output.
    #
    if length and verbose:
      print "%s Data found." % item('prompt_bullet')
    elif verbose:
      print '%s Data not found.' % item('prompt_warn')

    # Store JSON.
    if length and make_json:
      j_path = p.join(DATA_DIR, 'data', '%s_%s_data.json' % (db_table, index))

      with open(j_path, 'w') as outfile:
        json.dump(data, outfile)

    # Store CSV.
    if length and make_csv:
      c_path = p.join(DATA_DIR, 'data', '%s_%s_data.csv' % (db_table, index))
      f = csv.writer(open(c_path, "wb+"))
      f.writerow(data[0].keys())
      [f.writerow(flatten_row(row, preferred_fields).values()) for row in data]

    #
    # Storing results in DB.
    #
    if length and store_db:
      [
        StoreRecords([flatten_row(row, preferred_fields)], db_table, verbose)
        for row in data]


def BuildQueue(endpoint, config_path, verbose=False):
  '''Building the URL queues for the async requests.'''

  print '%s Building URL queue for `%s`.' % (item('prompt_bullet'), endpoint)
  url_list = []

  #
  # Fetching the parameters.
  #
  config = Config.LoadConfig(config_path)
  l = Config.LoadListOfLocations(config)
  parameters_dict = [AssembleLocationCodes(row=row) for row in l]

  #
  # Iterating over each of the parameter combinations.
  #
  for parameters in parameters_dict:

    #
    # Iterating over IDs and CSI types.
    #
    type_ids = ['1', '2', '3']

    for type in type_ids:
      parameters["indTypeID"] = type

      try:

        #
        # Query Income and FSC.
        #
        if endpoint is 'FCS':
          u = BuildQueryString('FCS', config, parameters)
          url_list.append(u)

        if endpoint is 'Income':
          u = BuildQueryString('Income', config, parameters)
          url_list.append(u)

        #
        # Add extra parameter for CSI.
        #
        if endpoint is 'CSI':
          csi_types = ['r', 'cs']
          for csi_type in csi_types:
            parameters["type"] = csi_type
            u = BuildQueryString('CSI', config, parameters)
            url_list.append(u)

      except Exception as e:
        if verbose:
          print e
        else:
          print "%s Failed to create URL list." % item('prompt_error')

  #
  # Returning the complete url list
  # for specific endpoint.
  #
  print '%s `%s` has %s URLs to query.' % (item('prompt_bullet'), endpoint, str(len(url_list)))
  return url_list


def MakeRequests(data, endpoint, config_path, **kwargs):
  '''Wrapper. query_limit determines the size of the url array.'''
  data_dir = kwargs['data_dir']
  query_limit = kwargs.get('query_limit', 2500)
  config = Config.LoadConfig(config_path)

  #
  # Load list of locations.
  #
  l = Config.LoadListOfLocations(config)

  #
  # Load endpoint information.
  #
  endpoint_info = Config.LoadEndpointInformation(endpoint, config)


  #
  # Divide the arrays into chunks and store in db.
  #
  def _chunks(data, n):
    ''' Yield successive n-sized chunks from l.'''
    for i in xrange(0, len(data), n):
        yield data[i:i+n]

  #
  # Building query strings and making queries.
  #
  progress = 0
  max_value = len(list(_chunks(data, query_limit)))
  widgets = [item('prompt_bullet'), ' Querying data for: {endpoint}'.format(endpoint=endpoint), pb.Percentage(), ' ', pb.Bar('-'), ' ', pb.ETA(), ' ']
  pbar = pb.ProgressBar(widgets=widgets, maxval=max_value).start()

  for query_list in list(_chunks(data, query_limit)):

    #
    # Make async queries.
    #
    QueryWFP(query_list, endpoint, endpoint_info, data_dir=data_dir)

    #
    # Updating progress bar.
    #
    pbar.update(progress)
    progress += 1

  pbar.finish()


def Main(config_path, data_dir, clean_run=True, verbose=True):
  '''Wrapper.'''

  try:
    endpoint_list = ['FCS', 'CSI', 'Income']
    for endpoint in endpoint_list:

      #
      # Clean records from database.
      #
      if clean_run:
        db.CleanTable(table_name=endpoint, verbose=True)

      #
      # Query WFP for data.
      #
      data = BuildQueue(endpoint, config_path, verbose=verbose)
      MakeRequests(data, endpoint, config_path, data_dir=data_dir)

    #
    # Success!
    #
    print "%s All data was collected successfully." % item('prompt_success')

  except Exception as e:
    print "%s Failed to collect data from WFP." % item('prompt_error')

    if verbose:
      print e
