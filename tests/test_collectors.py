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

