#!/bin/bash

#
# Installing virtual environment.
#
virtualenv venv
source venv/bin/activate

#
# Installing Python requirements
# and running collector configuration.
#
pip install -r requirements.txt
python scripts/config/
