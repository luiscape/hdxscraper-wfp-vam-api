#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
import json

# Below as a helper for namespaces.
# Looks like a horrible hack.
dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

import sqlite3 as SQLite
from utilities.prompt_format import item


def CleanTable(table, database_file = 'scraperwiki.sqlite', verbose=True):
  '''Clean all records from table in database.'''

  #
  # Connect to database.
  #
  conn = SQLite.connect(database_file)
  Cursor = conn.cursor()

  #
  # Build SQL statement.
  #
  print '%s Cleaning table `%s`.' % (item('prompt_bullet'), table)
  statement = 'DELETE FROM {table}'.format(table=table)

  #
  # SQL execution.
  #
  try:

    #
    # Execute SQL statement.
    #
    Cursor.execute(statement)

    #
    # Close the connection.
    #
    conn.commit()
    Cursor.close()

    if verbose:
      print '%s Table `%s` cleaned successfully.' % (item('prompt_bullet'), table)

    return True

  except Exception as e:
    if verbose:
      print '%s Failed to clean table `%s`.' (item('prompt_error'), table)
      print e

    return False



def StoreRecords(data, table, database_file='scraperwiki.sqlite', unlock_seconds=5, verbose=True):
  '''Store records in a ScraperWiki database.'''

  # Available schemas.
  schemas = {
    'FCS': ["ADM0_ID", "ADM5_ID", "Methodology", "LivelihoodZoneName", "ADM4_ID", "FCS_borderline", "FCS_month", "IndicatorTypeID", "FCS_dataSource", "methodologyID", "FCS_year", "TargetGroup", "ADM3_ID", "ADM2_ID", "Lz_ID", "mr_id", "FCS_lowerThreshold", "FCS_id", "FCS_poor", "targetGroupID", "ADM1_ID", "FCS_upperThreshold", "FCS_acceptable", "FCS_mean"],
    'CSI': ["CSI_rMediumCoping", "IndicatorTypeID", "ADM0_ID", "CSI_csHighCoping", "ADM5_ID", "LivelihoodZoneName", "ADM4_ID", "CSI_rDataSource", "CSI_csLowCoping", "MethodologyCs", "csMethodologyID", "CSI_rHighCoping", "CSI_id", "CSI_rMediumHighThreshold", "CSI_csMean", "CSI_rLowCoping", "CSI_rLowMediumThreshold", "rMethodologyID", "CSI_rMonth", "csTargetGroupID", "CSI_rNoCoping", "TargetGroupCs", "ADM3_ID", "CSI_csDataSource", "ADM2_ID", "TargetGroupR", "CSI_csLowMediumThreshold", "Lz_ID", "MethodologyR", "CSI_csMediumCoping", "mr_id", "CSI_csNoCoping", "CSI_rYear", "fdc", "CSI_csMediumHighThreshold", "rTargetGroupID", "CSI_csYear", "CSI_rMean", "ADM1_ID", "CSI_csMonth"],
    'Income': ["IncomeSubCategoryID", "IncomeID", "Adm4_ID", "Adm0_ID", "IncomeYear", "Adm3_ID", "IndicatorTypeID", "Adm2_ID", "IncomeCategoryID", "Adm5_ID", "IncomeSubCategory", "IncomeCategory", "IncomeMonth", "mr_id", "IncomeValue", "Adm1_ID"],
    'Gaul': ["ADM_ID","CONTINENT","REGION","UN_CODE","ISO3","WFP_ISO3","ADM0_NAME","ADM0_CODE","ADM1_NAME","ADM1_CODE","ADM2_NAME","ADM2_CODE","ADM3_NAME","ADM3_CODE","ADM4_NAME","ADM4_CODE","ADM5_NAME","ADM5_CODE","SALB0","SALB1","SALB2","STR_YEAR0","STR_YEAR1","STR_YEAR2","STR_YEAR3","STR_YEAR4","STR_YEAR5","EXP_YEAR0","EXP_YEAR1","EXP_YEAR2","EXP_YEAR3","EXP_YEAR4","EXP_YEAR5","LAST_UPDAT"]
  }

  #
  # Connect to database..
  #
  conn = SQLite.connect(database_file)
  Cursor = conn.cursor()

  try:
    schema = schemas[table]

  except Exception as e:

    if verbose is True:
      print "%s select one of the following tables: %s." % (item('prompt_error'), ", ".join(schemas.keys()))
      print e

    print '%s Could not find schema.' % item('prompt_error')
    return False

  with conn:
    try:
      for record in data:

        if verbose:
          print json.dumps(record)

        #
        # Storing record.
        #
        n_values_string = ('?,' * len(record))[:-1]
        Cursor.execute('INSERT INTO {table} VALUES ({n_values_string})'.format(table=table, n_values_string=n_values_string), record.values())
        time.sleep(unlock_seconds)

        print '%s Record stored successfully.' % item('prompt_bullet')
        return True

      #
      # Commit and close connection.
      #
      conn.commit()
      conn.close()
      Cursor.close()


    except Exception as e:
      if verbose:
        print "%s Failed to store record in database." % item('prompt_error')
        print e

      return False

