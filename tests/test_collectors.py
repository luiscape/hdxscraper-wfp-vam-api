#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import mock
import unittest
import scraperwiki
from mock import patch

from scripts.utilities import db as DB
from scripts.config import setup as Setup
from scripts.config import config as Config
from scripts.wfp_collect.collect import SelectPreferredField
from scripts.wfp_collect.build_url import BuildQueryString
from scripts.wfp_collect.build_url import AssembleLocationCodes


class BuildURLsTest(unittest.TestCase):
  '''Testing the process of creating a database.'''

  def test_output_of_assemble_location_codes(self):
    l = Config.LoadListOfLocations()
    for row in l:
      assert type(AssembleLocationCodes(row)) == dict


  def test_building_query_strings(self):
    l = Config.LoadListOfLocations()
    l = l[0:10]

    #
    # Testing that every url
    # is a string.
    #
    parameters_dict = []
    endpoints = ['CSI', 'FCS', 'Income']
    for row in l:
      parameters_dict.append(AssembleLocationCodes(row=row))
      for i in range(0,len(parameters_dict)):
        parameters = parameters_dict[i]
        for e in endpoints:
          u = BuildQueryString(endpoint=e, parameters_dict=parameters)
          print u
          assert type(u) == unicode


    odd_parameters = [{ 'foo': 4, 'bar': 7 }]
    for parameters in odd_parameters:
        for e in endpoints:
          assert BuildQueryString(endpoint=e, parameters_dict=parameters) == False



class CollectingDataFromWFP(unittest.TestCase):
  '''Testing schemas, availability of the API, and alike.'''

  def test_storing_record_csi(self):
    N_records = 10000
    endpoint_info = Config.LoadEndpointInformation('CSI', verbose=True)
    data = Config.LoadConfig(os.path.join('tests', 'data', 'test_data_csi.json'))
    records = []
    for row in data:
      record = { key:row[key] if isinstance(row[key], dict) is False else row[key][SelectPreferredField(endpoint_info, key)] for key in row.keys() }
      for i in range(0, N_records):
        records.append(record)

    assert DB.StoreRecords(records, table='CSI') == True

  def test_storing_record_fcs(self):
    N_records = 10000
    endpoint_info = Config.LoadEndpointInformation('FCS', verbose=True)
    data = Config.LoadConfig(os.path.join('tests', 'data', 'test_data_fcs.json'))
    records = []
    for row in data:
      record = { key:row[key] if isinstance(row[key], dict) is False else row[key][SelectPreferredField(endpoint_info, key)] for key in row.keys() }
      for i in range(0, N_records):
        records.append(record)

    assert DB.StoreRecords(records, table='FCS') == True

  def test_storing_record_income(self):
    N_records = 10000
    endpoint_info = Config.LoadEndpointInformation('Income', verbose=True)
    data = Config.LoadConfig(os.path.join('tests', 'data', 'test_data_income.json'))
    records = []
    for row in data:
      record = { key:row[key] if isinstance(row[key], dict) is False else row[key][SelectPreferredField(endpoint_info, key)] for key in row.keys() }
      for i in range(0, N_records):
        records.append(record)

    assert DB.StoreRecords(records, table='Income') == True


  # def test_schema_fcs(self):

  # def test_schema_csi(self):

  # def test_schema_income(self):

