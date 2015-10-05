#!/bin/bash

#
# Installing virtual environment.
# And the latest version of pip.
#
virtualenv venv
source venv/bin/activate
pip install --upgrade pip

#
# Installing Python requirements
# and running collector configuration.
#
pip install -r tool/requirements.txt
python tool/scripts/config/
