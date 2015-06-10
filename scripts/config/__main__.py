#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import setup as Setup

from os import path as p
from scripts.utilities.prompt_format import item

DATA_DIR = p.dirname(p.dirname(p.dirname(__file__)))
CONFIG_PATH = p.join(DATA_DIR, 'config', 'config.json')


def Main(config_path):
  '''Wrapper.'''
  Setup.CreateTables(config_path)

if __name__ == '__main__':
  Main(CONFIG_PATH)
