FROM python:latest

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y
RUN ACCEPT_EULA=Y apt-get install -y python3-venv

ENV APPDIR /opt/alpaca-ingester
RUN mkdir -p $APPDIR
WORKDIR $APPDIR
RUN mkdir /config

ARG VENV=$APPDIR/venv
RUN python3 -m venv $VENV 
ENV PATH "$VENV/bin:$PATH"

RUN python -m pip install --upgrade pip
RUN pip install --upgrade setuptools wheel

COPY app app
COPY main.py logging.yaml requirements.txt boot.sh ./
COPY config.yaml ./sample.yaml

RUN chmod +x boot.sh

RUN pip install -r requirements.txt

ENTRYPOINT ["./boot.sh"]