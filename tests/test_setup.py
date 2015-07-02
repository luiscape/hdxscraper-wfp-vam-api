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


class DatabaseCreationTest(unittest.TestCase):
  '''Testing the process of creating a database.'''

  def test_creating_database(self):
    assert Setup.CreateTables() == True

  def test_tables_exist(self):
    tables = scraperwiki.sqlite.show_tables()
    assert 'FCS' in tables.keys()
    assert 'CSI' in tables.keys()
    assert 'Income' in tables.keys()


class SWDatabaseManagementTest(unittest.TestCase):
  '''Unit tests for the ScraperWiki database management scripts.'''

  def test_database_connection(self):
    p = scraperwiki.sqlite.show_tables()
    assert type(p) == dict

  def test_database_available(self):
    tables = scraperwiki.sqlite.show_tables()
    assert 'FCS' in tables.keys()
    assert 'CSI' in tables.keys()
    assert 'Income' in tables.keys()


class StoringRecordsTest(unittest.TestCase):
  '''Unit tests for the storing records mechanism.'''

  def test_storing_record_fsc(self):
    #
    # Running the JSON flattening function.
    #
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
    #
    # Running the JSON flattening function.
    #e
    N_records = 10000
    endpoint_info = Config.LoadEndpointInformation('Income', verbose=True)
    data = Config.LoadConfig(os.path.join('tests', 'data', 'test_data_income.json'))
    records = []
    for row in data:
      record = { key:row[key] if isinstance(row[key], dict) is False else row[key][SelectPreferredField(endpoint_info, key)] for key in row.keys() }
      for i in range(0, N_records):
        records.append(record)

    assert DB.StoreRecords(records, table='Income') == True

