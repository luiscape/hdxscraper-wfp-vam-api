#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import scraperwiki
import progressbar as pb

from scripts.utilities.prompt_format import item


def StoreRecords(data, schema, table):
  '''Store records in a ScraperWiki database.'''

  try:
    for record in data:
      scraperwiki.sqlite.save(schema, record, table_name=table)

  except Exception as e:
    print "%s Failed to store record in database." % item('prompt_error')
    print e
