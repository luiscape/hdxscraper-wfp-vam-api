#!/bin/bash

#
# Installing virtual environment.
# And the latest version of pip.
#
virtualenv venv
pip install --upgrade pip
source venv/bin/activate

#
# Installing Python requirements
# and running collector configuration.
#
pip install -r tool/requirements.txt
python tool/scripts/config/
