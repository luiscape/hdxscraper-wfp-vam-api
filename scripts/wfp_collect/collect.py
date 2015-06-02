#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import csv
import json
import scraperwiki
import progressbar as pb
import grequests as requests

# Below as a helper for namespaces.
# Looks like a horrible hack.
dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

from math import ceil
from utilities import db
from utilities.prompt_format import item
from utilities.store_records import StoreRecords

from config import config as Config
from wfp_collect.build_url import BuildQueryString
from wfp_collect.build_url import AssembleLocationCodes

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]


def QueryWFP(url_list, db_table, verbose = False, make_json = False, make_csv = False, store_db = True):
  '''Query WFP's VAM API asyncronousy.'''

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
        print "%s connection with the API failed." % item('promt_error')
    

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
          f.writerow([ row[key] if isinstance(row[key], dict) is False else row[key].values()[2] for key in row.keys() ])
      
      #
      # Storing results in DB.
      #
      if store_db:
        for row in data:
          #
          # Here we have to select the right values
          # from the nested fields.
          #
          record = [{ key:row[key] if isinstance(row[key], dict) is False else row[key].values()[2] for key in row.keys() }]
          StoreRecords(record, db_table, verbose=True)

      
      #
      # Index for storing the data in CSV and JSON.
      #
      index += 1


def CreateURLArray(array, endpoint, parameters_dict):
  '''Creating an array of URLS to be passed to the async querier.'''

  u = BuildQueryString(endpoint, parameters_dict)

  try:
    array.append(u)

  except Exception as e:
    print '%s Could not create URL array.' % item('prompt_error')
    print e


def BuildQueue(endpoint):
  '''Building the URL queues for the async requests.'''
  
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



def MakeRequests(data, endpoint, query_limit, verbose=True):
  '''Wrapper. query_limit determines the size of the url array.'''
  
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
 
  for query_list in list(_chunks(data, query_limit)):
    
    #
    # Make async queries.
    #
    QueryWFP(url_list=query_list, db_table=endpoint)

    #
    # Updating progress bar.
    #
    pbar.update(progress)
    progress += 1
 
  pbar.finish()

    


def Main(clean_run=True, verbose=True):
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
      data = BuildQueue(endpoint)
      MakeRequests(data, endpoint, query_limit=2500)

    
    #
    # Success!
    #
    print "%s All data was collected successfully." % item('prompt_success')


  except Exception as e:
    print "%s Failed to collect data from WFP." % item('prompt_error')
    if verbose:
      print e
