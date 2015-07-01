#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

import setup as Setup
# import gaul as Gaul
from utilities.prompt_format import item


def Main():
  '''Wrapper.'''
  Setup.CreateTables()
  #Gaul.Main()

if __name__ == '__main__':
  Main()
