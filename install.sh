#!/bin/bash
echo je_Suis_Un
pip install virtualenv
virtualenv --python python3.10 venv
source venv/bin/activate
python3.10 -m pip install --upgrade pip
pip install -r requirements.txt
python3.10 src/hyperpoly/HyperPoly.py
