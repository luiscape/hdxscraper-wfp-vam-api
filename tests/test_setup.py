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
