FROM python:3.11

RUN apt-get update
RUN apt-get install -y firefox-esr

WORKDIR /usr/resource

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux-aarch64.tar.gz
RUN tar -xvzf geckodriver-v0.33.0-linux-aarch64.tar.gz
RUN rm geckodriver-v0.33.0-linux-aarch64.tar.gz
RUN mv geckodriver /usr/local/bin/
RUN chmod +x /usr/local/bin/geckodriver

WORKDIR /usr/src/app

COPY . .

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

CMD [ "python", "src/hyperpoly/HyperPoly.py" ]