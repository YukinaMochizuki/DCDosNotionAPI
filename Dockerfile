FROM python:slim

COPY requirements.txt /tmp/

RUN apt update && apt install -y git
RUN pip install -r /tmp/requirements.txt

RUN mkdir /app
WORKDIR /app
COPY main.py main.py
COPY config.ini config.ini

CMD [ "python", "main.py" ]
