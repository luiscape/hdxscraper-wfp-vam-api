#!/bin/bash

virtualenv venv
source tool/venv/bin/activate

pip install -r requirements.txt
pip install requests[security]

