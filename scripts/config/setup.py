#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import scraperwiki
import config as Config

from os import path as p
from scripts.utilities.prompt_format import item


def CreateTables(config_path, verbose=True):
  '''Creating the tables of the new database.'''


  try:
    endpoints = Config.LoadConfig(config_path)

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
  CreateTables(Config.CONFIG_PATH)
