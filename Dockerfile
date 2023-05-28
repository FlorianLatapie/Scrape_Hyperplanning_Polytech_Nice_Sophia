FROM python:3.10

WORKDIR /usr/resource

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux-aarch64.tar.gz

#ADD geckodriver-v0.33.0-linux-aarch64.tar.gz .
#
#RUN sudo mv geckodriver /usr/local/bin/
#
#RUN sudo chmod +x /usr/local/bin/geckodriver
#
#RUN geckodriver --version
#
#WORKDIR /usr/src/app
#
#COPY . .
#
#RUN pip install -r requirements.txt

CMD [ "python", "wait.py" ]