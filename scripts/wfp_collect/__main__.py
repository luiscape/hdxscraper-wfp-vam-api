#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import scraperwiki

# Below as a helper for namespaces.
# Looks like a horrible hack.
dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

from config import config as Config
from wfp_collect import collect


if __name__ == '__main__':
  try:
    sys.argv[1]
    config_path = Config.DEV_CONFIG_PATH
    kwargs = {'query_limit': 10}
    print "Running in development mode."

  except IndexError:
    config_path = Config.CONFIG_PATH
    kwargs = {'query_limit': 50}

  kwargs['data_dir'] = Config.DATA_DIR
  collect.Main(config_path, **kwargs)
