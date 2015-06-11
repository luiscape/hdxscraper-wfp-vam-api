#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import scraperwiki
import progressbar as pb

from scripts.utilities.prompt_format import item


def StoreRecords(data, table, verbose=False):
  '''Store records in a ScraperWiki database.'''

  # Available schemas.
  schemas = {
    'FCS': [
      "ADM0_ID", "ADM5_ID", "Methodology", "LivelihoodZoneName", "ADM4_ID",
      "FCS_borderline", "FCS_month", "IndicatorTypeID", "FCS_dataSource",
      "methodologyID", "FCS_year", "TargetGroup", "ADM3_ID", "ADM2_ID",
      "Lz_ID", "mr_id", "FCS_lowerThreshold", "FCS_id", "FCS_poor",
      "targetGroupID", "ADM1_ID", "FCS_upperThreshold", "FCS_acceptable",
      "FCS_mean"
    ],
    'CSI': [
      "CSI_rMediumCoping", "IndicatorTypeID", "ADM0_ID", "CSI_csHighCoping",
      "ADM5_ID", "LivelihoodZoneName", "ADM4_ID", "CSI_rDataSource",
      "CSI_csLowCoping", "MethodologyCs", "csMethodologyID", "CSI_rHighCoping",
      "CSI_id", "CSI_rMediumHighThreshold", "CSI_csMean", "CSI_rLowCoping",
      "CSI_rLowMediumThreshold", "rMethodologyID", "CSI_rMonth",
      "csTargetGroupID", "CSI_rNoCoping", "TargetGroupCs", "ADM3_ID",
      "CSI_csDataSource", "ADM2_ID", "TargetGroupR", "CSI_csLowMediumThreshold",
      "Lz_ID", "MethodologyR", "CSI_csMediumCoping", "mr_id", "CSI_csNoCoping",
      "CSI_rYear", "fdc", "CSI_csMediumHighThreshold", "rTargetGroupID",
      "CSI_csYear", "CSI_rMean", "ADM1_ID", "CSI_csMonth"
    ],
    'Income': [
      "IncomeSubCategoryID", "IncomeID", "Adm4_ID", "Adm0_ID", "IncomeYear",
      "Adm3_ID", "IndicatorTypeID", "Adm2_ID", "IncomeCategoryID", "Adm5_ID",
      "IncomeSubCategory", "IncomeCategory", "IncomeMonth", "mr_id",
      "IncomeValue", "Adm1_ID"
    ]
  }

  try:
    schema = schemas[table]

  except Exception as e:

    if verbose is True:
      print "%s select one of the following tables: %s." % (item('prompt_error'), ", ".join(schemas.keys()))
      print e

    print '%s Could not find schema.' % item('prompt_error')
    return False

  try:
    for record in data:
      scraperwiki.sqlite.save(schema, record, table_name=table)

  except Exception as e:
    print "%s Failed to store record in database." % item('prompt_error')
    print e
