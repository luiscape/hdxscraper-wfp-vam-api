#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import setup as Setup
import config as Config

from os import path as p
from scripts.utilities.prompt_format import item


def Main(config_path):
  '''Wrapper.'''
  Setup.CreateTables(config_path)

if __name__ == '__main__':
  Main(Config.CONFIG_PATH)
