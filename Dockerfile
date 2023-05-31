FROM python:3.14

RUN apt-get update && apt-get install -y firefox-esr

WORKDIR /usr/resource

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux-aarch64.tar.gz \
    && tar -xvzf geckodriver-v0.33.0-linux-aarch64.tar.gz \
    && rm geckodriver-v0.33.0-linux-aarch64.tar.gz \
    && mv geckodriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/geckodriver \
    && geckodriver --version

WORKDIR /usr/src/app

COPY . .

RUN apt-get install python3-venv  \
    && python3 -m venv venv  \
    && chmod +x ./venv/bin/activate  \
    && ./venv/bin/activate  \
    && pip3 install --upgrade pip  \
    && pip3 install -r requirements.txt

CMD [ "python", "src/hyperpoly/HyperPoly.py" ]