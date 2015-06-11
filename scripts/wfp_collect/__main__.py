#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import scraperwiki

from scripts.config import config as Config
from scripts.wfp_collect import collect


if __name__ == '__main__':
  if sys.argv[1]:
    config_path = Config.DEV_CONFIG_PATH
    print "Running in development mode."
  else:
    config_path = Config.CONFIG_PATH

  try:
      collect.Main(config_path, Config.DATA_DIR)
      print "SW Status: Everything seems to be just fine."
      scraperwiki.status('ok')
  except Exception as e:
      print e
      scraperwiki.status('error', 'Error collecting data.')
