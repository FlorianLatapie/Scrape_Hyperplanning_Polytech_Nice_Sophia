python3.10 -m venv venv
call venv\Scripts\activate.bat
python.exe -m pip install --upgrade pip
pip3.10 install -r requirements.txt

python3.10 src/hyperpoly/HyperPoly.py