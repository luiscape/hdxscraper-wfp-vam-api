#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

# Below as a helper for namespaces.
# Looks like a horrible hack.
dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

from wfp_collect import collect 


if __name__ == '__main__':

  collect.Main()

  # try:
  #     collect.Main()
  #     print "SW Status: Everything seems to be just fine."
  #     scraperwiki.status('ok')

  # except Exception as e:
  #     print e
  #     scraperwiki.status('error', 'Error collecting data.')
  #     os.system("echo https://ds-ec2.scraperwiki.com/deudwxf/bfbenh2isykhn56/http/log.txt | mail -s 'WFP APIs: Failed collecting data.' luiscape@gmail.com")
