#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

# Below as a helper for namespaces.
# Looks like a horrible hack.
dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

import scraperwiki
import progressbar as pb

from utilities import prompt_format as I

def StoreRecords(data, table, verbose = True):
  '''Store records in a ScraperWiki database.'''

  # Available schemas.
  # Still in development.
  schemas = {
    'nodes': ['name', 'topic'],
    'links': ['source', 'value', 'target']
  }

  try:
    schema = schemas[table]

  except Exception as e:

    if verbose:
      print e
      return False

    else: 
      print "%s select one of the following tables: 'nodes' or 'links." % I.item('prompt_error')
      return False


  ## See if record already exists.
  def recordExists(record):

    ## TODO: navigate the schema properly.
    
    key1 = str(record[schema[0]])
    key2 = str(record[schema[1]])
    sql_statement = 'SELECT COUNT (' + schema[0] + ') FROM ' + table + ' WHERE ' + schema[0] + '=' + '"' + key1 + '"' + ' AND ' + schema[1] + '=' + '"' + key2 + '"'
    
    try:
      query = scraperwiki.sqlite.execute(sql_statement)
      return query["data"][0][0] > 0

    except Exception as e:
      print e
      return

  
      
  def recordDelete(record):
    key1 = str(record[schema[0]])
    key2 = str(record[schema[1]])
    sql_statement = 'DELETE FROM ' + table + ' WHERE ' + schema[0] + '=' + '"' + key1 + '"' + ' AND ' + schema[1] + '=' + '"' + key2 + '"'

    try:
      query = scraperwiki.sqlite.execute(sql_statement)

    except Exception as e:
      print e


  exist = 0
  not_exist = 0
  progress = 0
  total_records = len(data)
  widgets = [I.item('prompt_bullet'), ' Storing in db:', pb.Percentage(), ' ', pb.Bar('-'), ' ', pb.ETA(), ' ']
  pbar = pb.ProgressBar(widgets=widgets, maxval=total_records).start()
  for record in data:
    
    #
    # Progress bar.
    #
    if verbose:
      # progress_bar = round((float(progress) / total_records), 4) * 100
      # print I.item('prompt_bullet') + ' ' + table + ' progress: ' + str(progress_bar) + '%'
      pbar.update(progress)

    if recordExists(record) is True:
      recordDelete(record)
      exist += 1

    else: 
      not_exist += 1

    scraperwiki.sqlite.save(schema, record, table_name=table)

    progress += 1


  # Printing summary of operation.
  if not_exist > 0:
    if verbose:
      print "%s Storing %s record(s) in database, %s." % (I.item('prompt_bullet'), not_exist, table)

  if exist > 0:
    print "%s %s records already exists in database, %s. Updated." % (I.item('prompt_bullet'), exist, table)

  return True


if __name__ == '__main__':
  StoreRecords()