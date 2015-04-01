#!/usr/bin/python
# -*- coding: utf-8 -*-

from termcolor import colored as color

def item(i):
  dictionary = {
    'prompt_bullet': color(" →", "blue", attrs=['bold']),
    'prompt_error':  color(" ERROR:", "red", attrs=['bold']),
    'prompt_success': color(" SUCCESS:", "green", attrs=['bold'])
  }
  return dictionary[i]