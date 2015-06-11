#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

# Below as a helper for namespaces.
# Looks like a horrible hack.
dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

import csv
import json
import scraperwiki

from utilities.prompt_format import item
from utilities.store_records import StoreRecords

def CreateDBTable(table_name='Gaul', verbose=True):
  '''Creating the GAUL db table.'''

  db_fields = ["ADM_ID","CONTINENT","REGION","UN_CODE","ISO3","WFP_ISO3","ADM0_NAME","ADM0_CODE","ADM1_NAME","ADM1_CODE","ADM2_NAME","ADM2_CODE","ADM3_NAME","ADM3_CODE","ADM4_NAME","ADM4_CODE","ADM5_NAME","ADM5_CODE","SALB0","SALB1","SALB2","STR_YEAR0","STR_YEAR1","STR_YEAR2","STR_YEAR3","STR_YEAR4","STR_YEAR5","EXP_YEAR0","EXP_YEAR1","EXP_YEAR2","EXP_YEAR3","EXP_YEAR4","EXP_YEAR5","LAST_UPDAT"]
  statement = " TEXT, ".join(db_fields)
  statement = 'CREATE TABLE IF NOT EXISTS %s(%s TEXT)' % (table_name, statement)

  try:
    scraperwiki.sqlite.execute(statement)
    scraperwiki.sqlite._State.new_transaction()
    print "%s table `%s` created." % (item('prompt_bullet'), str(table_name))

  except Exception as e:
    print '%s Table `%s` could not be created.' % (item('prompt_error'), table_name)
    if verbose:
      print e
    return False


def CollectAndStoreGaulData(csv_name, db_table='Gaul', verbose=True):
  '''Use a CSV file to store the WFP-modified GAUL on a local database.'''

  print '%s Storing GAUL database in DB (~5 mins).' % item('prompt_bullet')
  
  #
  # Data dir.
  #
  data_dir = os.path.split(dir)[0]
  gaul_location = os.path.join(data_dir, 'config', csv_name)
  
  #
  # Storing GAUL on database.
  #
  try:
    with open(gaul_location) as csv_file:
      data = csv.DictReader(csv_file)
      records = []
      for row in data:
        StoreRecords(row, db_table, verbose=True)
        records.append(row)
        
#      StoreRecords(records, db_table, verbose=True)

  except Exception as e:
    print "%s Failed to store GAUL database in DB." % item('prompt_error')
    if verbose:
      print e
    return False
  



def Main():
  '''Wrapper.'''
  
  #
  # Creating table and storing records.
  #
  CreateDBTable()

  if CollectAndStoreGaulData('modified_admin_units.csv') is not False:
    print '%s Stored GAUL database on DB successfully.' % item('prompt_success')


if __name__ == '__main__':
  Main()