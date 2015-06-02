#!/bin/bash

# virtualenv venv
source venv/bin/activate

pip install -r tool/requirements.txt
pip install https://github.com/agsimeonov/grequests/archive/master.zip

python tool/scripts/config/