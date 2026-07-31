# GitOps Microservice Example

## This is the world for doodle

## Branches

- `main` — clean baseline; no OTel or New Relic instrumentation.
- `otel` — OpenTelemetry + New Relic NRDOT instrumentation, for Docker/Kubernetes deployments.
- `azure-functions-newrelic` — Azure Functions adapter (`azure-functions/`), instrumented with the New Relic Python agent. Branched from `main`.

Must add annotation to have New Relic scrape prometheus metrics like so

``` POD=`k get pods -n supreme-doodle | grep -i world | grep -v  ruby | grep Running | awk '{print $1}' `; k annotate pods $POD -n supreme-doodle   newrelic.io/scrape="true" ```
