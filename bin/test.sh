#!/bin/bash

source venv/bin/activate
nosetests --no-byte-compile --with-coverage
