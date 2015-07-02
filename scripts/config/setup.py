#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import scraperwiki

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

import config as Config
from utilities.prompt_format import item


def CreateTables(config_file='dev.json', verbose=True):
  '''Creating the tables of the new database.'''

  data_dir = os.path.split(dir)[0]

  try:
    endpoints = Config.LoadConfig(os.path.join(data_dir, 'config', config_file))

  except Exception as e:
    if verbose:
      print e
    else:
      print '%s Could not load configuration file.' % item('prompt_error')

  sql_statements = {}
  for endpoint in endpoints['endpoints']:
    table_name = endpoint['database']['name']
    statement = " TEXT, ".join(endpoint['database']['fields'])
    statement = 'CREATE TABLE IF NOT EXISTS %s(%s TEXT)' % (table_name, statement)
    sql_statements[table_name] = statement

  for table in sql_statements:
    try:
      query = scraperwiki.sqlite.execute(sql_statements[table])
      print "%s table `%s` created." % (item('prompt_bullet'), str(table))

    except Exception as e:
      print e
      return False


  print "%s Database created successfully." % item('prompt_success')
  return True


if __name__ == '__main__':
  CreateTables()
