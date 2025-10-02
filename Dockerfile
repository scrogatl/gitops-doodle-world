FROM python:3.10-slim-bullseye AS base

FROM base AS builder

RUN apt update && apt install git python3-pip -y
RUN apt install bash -y
RUN apt autoremove

FROM base

WORKDIR /world

COPY world/requirements.txt /world/requirements.txt
RUN pip3 install -r requirements.txt

ENV PYTHONUNBUFFERED=1

COPY world/src/ /world

EXPOSE 5002

ENV NEW_RELIC_APP_NAME=doodle-world

CMD flask run --host=0.0.0.0 -p 5002
#CMD newrelic-admin run-program flask run --host=0.0.0.0 -p 5002
#CMD opentelemetry-instrument --logs_exporter otlp flask run --debugger --host=0.0.0.0 -p 5002

