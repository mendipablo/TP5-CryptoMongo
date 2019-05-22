FROM python:3.6.7

ENV FLASK_APP api.py

RUN mkdir /app

WORKDIR /app

COPY main.py ./api.py

RUN pip3 install requests flask pymongo

ADD . /app

EXPOSE 5000

CMD FLASK_DEBUG=1 flask run --host=0.0.0.0
