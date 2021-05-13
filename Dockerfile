FROM python:3.8-slim

COPY requirements.txt /tmp/

RUN apt update && apt install -y git
RUN pip install -r /tmp/requirements.txt

RUN mkdir /app
WORKDIR /app
COPY main.py main.py

CMD [ "python", "main.py" ]
