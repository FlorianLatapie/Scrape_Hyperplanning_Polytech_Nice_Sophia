#!/bin/bash
pip install virtualenv
virtualenv --python python3.10 venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python3.10 src/hyperpoly/HyperPoly.py
