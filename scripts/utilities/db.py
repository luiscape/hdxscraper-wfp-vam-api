#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

# Below as a helper for namespaces.
# Looks like a horrible hack.
dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

import scraperwiki

from utilities.prompt_format import item


def CleanTable(table_name, verbose=True):
  '''Clean all records from table in database.'''

  #
  # SQL statement.
  #
  print '%s Cleaning table `%s`.' % (item('prompt_bullet'), table_name)
  sql = 'delete from {table_name}'.format(table_name=table_name)

  #
  # SQL execution.
  #
  try:
    scraperwiki.sqlite.execute(sql)
    if verbose:
      print '%s Table `%s` cleaned successfully.' % (item('prompt_bullet'), table_name)

  except Exception as e:
    if verbose:
      print '%s Failed to clean table `%s`.' (item('prompt_error'), table_name)
      print e
