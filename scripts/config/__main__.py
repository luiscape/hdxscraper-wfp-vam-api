#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import setup as Setup
import config as Config

# Below as a helper for namespaces.
# Looks like a horrible hack.
dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

from os import path as p
from utilities.prompt_format import item


if __name__ == '__main__':
  Setup.CreateTables(Config.CONFIG_PATH)
