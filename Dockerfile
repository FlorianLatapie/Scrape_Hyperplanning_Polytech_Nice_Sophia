FROM python:3.10

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

RUN python -m venv venv  \
    && ./venv/bin/activate  \
    && pip install --upgrade pip  \
    && pip install -r requirements.txt

CMD [ "python", "src/hyperpoly/HyperPoly.py" ]