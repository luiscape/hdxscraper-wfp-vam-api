#!/bin/bash

# virtualenv venv
source venv/bin/activate

pip install -r tool/requirements.txt
python tool/scripts/config/
