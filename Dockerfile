FROM python:3.10-slim-bullseye 

WORKDIR /world

COPY world/requirements.txt /world/requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 5002

ENV PYTHONUNBUFFERED=1
COPY world/src/ /world

ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
CMD ["newrelic-admin", "run-program", "flask", "run", "--host=0.0.0.0", "-p", "5002"]
