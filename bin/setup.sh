#!/bin/bash

# virtualenv venv
source venv/bin/activate

# https://cryptography.io/en/latest/installation/#using-your-own-openssl-on-os-x
pip install -r requirements.txt
python scripts/config/
