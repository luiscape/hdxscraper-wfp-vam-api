#!/bin/bash

# for now, this:
rm scraperwiki.sqlite

source venv/bin/activate
python code/scraper.py > http/log.csv