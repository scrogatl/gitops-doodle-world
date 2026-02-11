FROM python:3.10-slim-bullseye 

WORKDIR /world

COPY world/requirements.txt /world/requirements.txt
RUN pip3 install -r requirements.txt
RUN opentelemetry-bootstrap -a install

EXPOSE 5002

ENV PYTHONUNBUFFERED=1
COPY world/src/ /world
CMD flask run --host=0.0.0.0 -p 5002
#CMD newrelic-admin run-program flask run --host=0.0.0.0 -p 5002
#CMD opentelemetry-instrument --logs_exporter otlp flask run --debugger --host=0.0.0.0 -p 5002

