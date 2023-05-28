FROM python:3.10

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux-aarch64.tar.gz

tar -xvf geckodriver-v0.33.0-linux-aarch64.tar.gz

sudo mv geckodriver /usr/local/bin/

sudo chmod +x /usr/local/bin/geckodriver

geckodriver --version

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

CMD [ "python", "src/hyperpoly/HyperPoly.py" ]