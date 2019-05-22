FROM python:3.6.7

WORKDIR /app

RUN pip3 install requests flask pymongo

COPY main.py ./agent.py

ADD . /app

CMD [ "python3","agent.py" ]