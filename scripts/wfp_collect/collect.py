#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import csv
import json
import progressbar as pb
import grequests as requests

# Below as a helper for namespaces.
# Looks like a horrible hack.
dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

from math import ceil
from utilities import db
from utilities.db import StoreRecords
from utilities.prompt_format import item

from config import config as Config
from wfp_collect.build_url import BuildQueryString
from wfp_collect.build_url import AssembleLocationCodes

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]



def SelectPreferredField(endpoint_info, nested_key):
  '''Selects a prefered frield from a key input and an endpoint.'''

  #
  # Selectign fields that have to
  # be flattened from the config file.
  #
  nested_keys = endpoint_info['flattened_fields']

  #
  # Iterating over the fields.
  #
  for key in nested_keys:
    if key['nested_field'] == nested_key:
      return key['prefered_field']

  #
  # If preferred key not found,
  # return the first key.
  #
  return 0


def QueryWFP(url_list, db_table, verbose=False, make_json=False, make_csv=False, store_db=True):
  '''Query WFP's VAM API asyncronousy.'''

  #
  # Load endpoint information.
  #
  endpoint_info = Config.LoadEndpointInformation(db_table)

  if verbose:
    for url in url_list:
      print '%s query: %s' % (item('prompt_bullet'), url)

  #
  # Defining the asyncronous request.
  #
  def _handle(r, e):
    try:
      r
    except Exception as error:
      print "%s error with URL %s" % (item('prompt_error'), r.status_code)
      print error

  request_list = (requests.get(url) for url in url_list)
  responses = requests.map(request_list, exception_handler=_handle)

  index = 1
  for r in responses:

    try:
      data = r.json()

    except Exception as e:
      if verbose:
        print "%s connection with the API failed." % item('prompt_error')


    #
    # Check if there is data available and store output.
    #
    if len(data) == 0:
      if verbose:
        print '%s Data not found.' % item('prompt_warn')

    if len(data) > 0:
      if verbose:
        print "%s Data found." % item('prompt_bullet')

      #
      # Storing JSON.
      #
      if make_json:
        data_dir = os.path.split(dir)[0]
        j_path = os.path.join(data_dir, 'data/') + db_table + '_' + str(index) + '_data.json'
        with open(j_path, 'w') as outfile:
          json.dump(data, outfile)

      #
      # Storing CSV.
      #
      if make_csv:
        data_dir = os.path.split(dir)[0]
        c_path = os.path.join(data_dir, 'data/') + db_table + '_' + str(index) + '_data_.csv'

        f = csv.writer(open(c_path, "wb+"))
        f.writerow(data[0].keys())

        for row in data:

          #
          # Flattening JSON based on preferred keys.
          #
          f.writerow([ row[key] if isinstance(row[key], dict) is False else row[key][SelectPreferredField(endpoint_info, key)] for key in row.keys() ])

      #
      # Storing results in DB.
      #
      if store_db:
        records = []
        for row in data:

          #
          # Flattening JSON based on preferred keys
          # and appending it back an array.
          #
          record = { key:row[key] if isinstance(row[key], dict) is False else row[key][SelectPreferredField(endpoint_info, key)] for key in row.keys() }
          records.append(record)

        #
        # Return the records array for post processing.
        #
        return records


      #
      # Index for storing the data in CSV and JSON.
      #
      index += 1


def CreateURLArray(array, endpoint, parameters_dict, verbose=True):
  '''Creating an array of URLS to be passed to the async querier.'''

  #
  # Appeding URLs to
  # a provided array.
  #
  u = BuildQueryString(endpoint, parameters_dict)
  try:
    array.append(u)

  except Exception as e:
    if verbose:
      print '%s Could not create URL array.' % item('prompt_error')
      print e

    return False


def BuildQueue(endpoint, verbose=True):
  '''Building the URL queues for the async requests.'''

  if verbose:
    print '%s Building URL queue for `%s`.' % (item('prompt_bullet'),endpoint)

  url_list = []

  #
  # Fetching the parameters.
  #
  l = Config.LoadListOfLocations()

  parameters_dict = []
  for row in l:
    parameters_dict.append(AssembleLocationCodes(row=row))


  #
  # Iterating over each of the
  # parameter combinations.
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
          u = BuildQueryString(endpoint='FCS', parameters_dict=parameters)
          url_list.append(u)

        if endpoint is 'Income':
          u = BuildQueryString(endpoint='Income', parameters_dict=parameters)
          url_list.append(u)

        #
        # Add extra parameter for CSI.
        #
        if endpoint is 'CSI':
          csi_types = ['r', 'cs']
          for csi_type in csi_types:
            parameters["type"] = csi_type
            u = BuildQueryString(endpoint='CSI', parameters_dict=parameters)
            url_list.append(u)


      except Exception as e:
        print "%s Failed to create URL list." % item('prompt_error')
        if verbose:
          print e

        return False


  #
  # Returning the complete url list
  # for specific endpoint.
  #
  print '%s `%s` has %s URLs to query.' % (item('prompt_bullet'), endpoint, str(len(url_list)))
  return url_list



def MakeRequests(data, endpoint, query_limit, verbose=True):
  '''Wrapper. query_limit determines the size of the url array.'''

  #
  # Load list of locations.
  #
  l = Config.LoadListOfLocations()

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

  endpoint_records = []
  for query_list in list(_chunks(data, query_limit)):

    #
    # Make async queries.
    #
    records_chunk = QueryWFP(url_list=query_list, db_table=endpoint)

    if records_chunk != None and records_chunk > 0:

      endpoint_records + records_chunk
      if verbose:
        print '%s A total of %s records have been collected thus far.' % (item('prompt_bullet'), len(endpoint_records))

    #
    # Updating progress bar.
    #
    pbar.update(progress)
    progress += 1

  #
  # Return all endpoint collected records.
  #
  pbar.finish()
  return endpoint_records




def Main(clean_run=True, verbose=True):
  '''Wrapper.'''

  try:
    endpoint_list = ['FCS', 'CSI', 'Income']
    # endpoint_list = ['CSI']
    for endpoint in endpoint_list:

      #
      # Clean records from database.
      #
      if clean_run:
        db.CleanTable(table=endpoint, verbose=True)

      #
      # Query WFP for data.
      #
      data = BuildQueue(endpoint)
      endpoint_records = MakeRequests(data, endpoint, query_limit=2500)

      #
      # Storing all records for a
      # specific endpoint in database.
      #
      StoreRecords(endpoint_records, endpoint, verbose=True)


    #
    # Success!
    #
    print "%s All data was collected successfully." % item('prompt_success')


  except Exception as e:
    print "%s Failed to collect data from WFP." % item('prompt_error')
    if verbose:
      print e
