# One Dockerfile, three images. Pick the flavor with --target:
#   plain     no agent
#   newrelic  New Relic Python agent (newrelic-admin)
#   otel      OpenTelemetry auto-instrumentation (opentelemetry-instrument)
FROM python:3.11-slim AS base
WORKDIR /world
ENV PYTHONUNBUFFERED=1
COPY world/requirements.txt /world/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 5002

FROM base AS plain
COPY world/src/ /world
CMD ["flask", "run", "--host=0.0.0.0", "-p", "5002"]

FROM base AS newrelic
COPY world/requirements-newrelic.txt /world/requirements-newrelic.txt
RUN pip3 install --no-cache-dir -r requirements-newrelic.txt
COPY world/src/ /world
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
CMD ["newrelic-admin", "run-program", "flask", "run", "--host=0.0.0.0", "-p", "5002"]

FROM base AS otel
COPY world/requirements-otel.txt /world/requirements-otel.txt
RUN pip3 install --no-cache-dir -r requirements-otel.txt \
 && opentelemetry-bootstrap -a install
COPY world/src/ /world
ENV OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
CMD ["opentelemetry-instrument", "flask", "run", "--host=0.0.0.0", "-p", "5002"]
