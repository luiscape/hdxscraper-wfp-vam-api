#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

import setup as Setup
from utilities.prompt_format import item


def Main():
  '''Wrapper.'''
  Setup.CreateTables()

if __name__ == '__main__':
  Main()