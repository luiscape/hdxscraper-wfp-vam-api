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
from scripts.wfp_collect.build_url import BuildQueryString
from scripts.wfp_collect.build_url import AssembleLocationCodes


class BuildURLsTest(unittest.TestCase):
  '''Testing the process of creating a database.'''

  def test_output_of_assemble_location_codes(self):
    config_path = os.path.join('config', 'config.json')
    config = Config.LoadConfig(config_path)
    l = Config.LoadListOfLocations(config)
    for row in l:
      assert type(AssembleLocationCodes(row)) == dict
